#!/usr/bin/env python3
"""
Resource Monitor for Football Data Pipeline
==========================================

Monitors disk space, memory usage, and implements data compression
for the step1→step2→step7 pipeline.

Features:
- Real-time disk space monitoring
- Memory usage alerts for running processes
- Automatic file compression for old data
- Pipeline health reporting
- Alert thresholds and notifications
"""

import os
import sys
import json
import gzip
import shutil
import psutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Configuration
PIPELINE_DIR = Path("/root/6-4-2025")
MONITOR_LOG = PIPELINE_DIR / "resource_monitor.log"
ALERT_LOG = PIPELINE_DIR / "resource_alerts.log"

# Thresholds
DISK_SPACE_WARNING_GB = 5.0  # Warn when less than 5GB free
DISK_SPACE_CRITICAL_GB = 1.0  # Critical when less than 1GB free
MEMORY_WARNING_PERCENT = 80.0  # Warn when pipeline uses >80% memory
MEMORY_CRITICAL_PERCENT = 90.0  # Critical when pipeline uses >90% memory
FILE_AGE_COMPRESS_DAYS = 3  # Compress files older than 3 days
FILE_AGE_DELETE_DAYS = 14  # Delete files older than 14 days

# File patterns to monitor
FILE_PATTERNS = {
    "step1_daily": "step1_20*.json",
    "step1_current": "step1.json", 
    "step2_current": "step2.json",
    "step7_logs": "logs/step7_matches.md*",
    "pipeline_logs": "*.log"
}

class ResourceMonitor:
    def __init__(self):
        self.setup_logging()
        self.alerts = []
        
    def setup_logging(self):
        """Setup logging for resource monitor"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(MONITOR_LOG),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Separate alert logger
        self.alert_logger = logging.getLogger("alerts")
        alert_handler = logging.FileHandler(ALERT_LOG)
        alert_handler.setFormatter(logging.Formatter('%(asctime)s - ALERT - %(message)s'))
        self.alert_logger.addHandler(alert_handler)
        self.alert_logger.setLevel(logging.WARNING)
        
    def get_disk_usage(self):
        """Get disk usage statistics"""
        try:
            usage = shutil.disk_usage(PIPELINE_DIR)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            used_percent = (used_gb / total_gb) * 100
            
            return {
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "used_percent": round(used_percent, 2),
                "status": self._get_disk_status(free_gb)
            }
        except Exception as e:
            self.logger.error(f"Failed to get disk usage: {e}")
            return None
            
    def _get_disk_status(self, free_gb):
        """Determine disk status based on free space"""
        if free_gb < DISK_SPACE_CRITICAL_GB:
            return "CRITICAL"
        elif free_gb < DISK_SPACE_WARNING_GB:
            return "WARNING"
        else:
            return "OK"
            
    def get_memory_usage(self):
        """Get memory usage for pipeline processes"""
        try:
            # Find step1.py process
            pipeline_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_percent', 'memory_info']):
                try:
                    if proc.info['cmdline'] and any('step1.py' in arg for arg in proc.info['cmdline']):
                        memory_mb = proc.info['memory_info'].rss / (1024**2)
                        pipeline_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "memory_percent": round(proc.info['memory_percent'], 2),
                            "memory_mb": round(memory_mb, 2),
                            "cmdline": " ".join(proc.info['cmdline'])
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # System memory
            system_memory = psutil.virtual_memory()
            
            return {
                "system": {
                    "total_gb": round(system_memory.total / (1024**3), 2),
                    "used_gb": round(system_memory.used / (1024**3), 2),
                    "available_gb": round(system_memory.available / (1024**3), 2),
                    "used_percent": round(system_memory.percent, 2)
                },
                "pipeline_processes": pipeline_processes,
                "status": self._get_memory_status(pipeline_processes)
            }
        except Exception as e:
            self.logger.error(f"Failed to get memory usage: {e}")
            return None
            
    def _get_memory_status(self, processes):
        """Determine memory status based on pipeline process usage"""
        if not processes:
            return "NO_PIPELINE"
            
        max_memory_percent = max(proc['memory_percent'] for proc in processes)
        
        if max_memory_percent > MEMORY_CRITICAL_PERCENT:
            return "CRITICAL"
        elif max_memory_percent > MEMORY_WARNING_PERCENT:
            return "WARNING"
        else:
            return "OK"
            
    def get_file_sizes(self):
        """Get sizes of pipeline files"""
        try:
            file_info = {}
            total_size = 0
            
            for category, pattern in FILE_PATTERNS.items():
                files = list(PIPELINE_DIR.glob(pattern))
                category_size = 0
                category_files = []
                
                for file_path in files:
                    if file_path.is_file():
                        size_mb = file_path.stat().st_size / (1024**2)
                        age_days = (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days
                        
                        category_files.append({
                            "name": file_path.name,
                            "size_mb": round(size_mb, 2),
                            "age_days": age_days,
                            "path": str(file_path)
                        })
                        category_size += size_mb
                        total_size += size_mb
                        
                file_info[category] = {
                    "files": category_files,
                    "total_size_mb": round(category_size, 2),
                    "file_count": len(category_files)
                }
                
            return {
                "categories": file_info,
                "total_size_mb": round(total_size, 2),
                "total_size_gb": round(total_size / 1024, 2)
            }
        except Exception as e:
            self.logger.error(f"Failed to get file sizes: {e}")
            return None
            
    def compress_old_files(self, dry_run=False):
        """Compress old daily files to save space"""
        compressed_files = []
        errors = []
        
        try:
            # Find old step1 daily files
            cutoff_date = datetime.now() - timedelta(days=FILE_AGE_COMPRESS_DAYS)
            daily_files = PIPELINE_DIR.glob("step1_20*.json")
            
            for file_path in daily_files:
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if file_mtime < cutoff_date and not file_path.name.endswith('.gz'):
                    try:
                        if not dry_run:
                            # Compress the file
                            with open(file_path, 'rb') as f_in:
                                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            
                            # Remove original file
                            file_path.unlink()
                            
                        original_size = file_path.stat().st_size / (1024**2)
                        compressed_files.append({
                            "file": file_path.name,
                            "original_size_mb": round(original_size, 2),
                            "age_days": (datetime.now() - file_mtime).days,
                            "action": "compressed" if not dry_run else "would_compress"
                        })
                        
                    except Exception as e:
                        errors.append(f"Failed to compress {file_path}: {e}")
                        
        except Exception as e:
            errors.append(f"Compression scan failed: {e}")
            
        return {
            "compressed_files": compressed_files,
            "errors": errors,
            "dry_run": dry_run
        }
        
    def cleanup_old_files(self, dry_run=False):
        """Delete very old files to free space"""
        deleted_files = []
        errors = []
        
        try:
            cutoff_date = datetime.now() - timedelta(days=FILE_AGE_DELETE_DAYS)
            
            # Delete old compressed files
            old_files = list(PIPELINE_DIR.glob("step1_20*.json.gz")) + \
                       list(PIPELINE_DIR.glob("logs/step7_matches.md.*"))
            
            for file_path in old_files:
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if file_mtime < cutoff_date:
                    try:
                        file_size = file_path.stat().st_size / (1024**2)
                        
                        if not dry_run:
                            file_path.unlink()
                            
                        deleted_files.append({
                            "file": file_path.name,
                            "size_mb": round(file_size, 2),
                            "age_days": (datetime.now() - file_mtime).days,
                            "action": "deleted" if not dry_run else "would_delete"
                        })
                        
                    except Exception as e:
                        errors.append(f"Failed to delete {file_path}: {e}")
                        
        except Exception as e:
            errors.append(f"Cleanup scan failed: {e}")
            
        return {
            "deleted_files": deleted_files,
            "errors": errors,
            "dry_run": dry_run
        }
        
    def check_alerts(self, disk_info, memory_info):
        """Check for alert conditions"""
        alerts = []
        
        # Disk space alerts
        if disk_info and disk_info['status'] in ['WARNING', 'CRITICAL']:
            alert = {
                "type": "DISK_SPACE",
                "level": disk_info['status'],
                "message": f"Disk space {disk_info['status'].lower()}: {disk_info['free_gb']}GB free",
                "details": disk_info
            }
            alerts.append(alert)
            self.alert_logger.warning(f"DISK_SPACE_{disk_info['status']}: {alert['message']}")
            
        # Memory alerts
        if memory_info and memory_info['status'] in ['WARNING', 'CRITICAL']:
            alert = {
                "type": "MEMORY_USAGE", 
                "level": memory_info['status'],
                "message": f"Pipeline memory usage {memory_info['status'].lower()}",
                "details": memory_info
            }
            alerts.append(alert)
            self.alert_logger.warning(f"MEMORY_{memory_info['status']}: {alert['message']}")
            
        return alerts
        
    def generate_report(self):
        """Generate comprehensive resource report"""
        self.logger.info("Generating resource usage report...")
        
        # Collect all data
        disk_info = self.get_disk_usage()
        memory_info = self.get_memory_usage()
        file_info = self.get_file_sizes()
        compression_preview = self.compress_old_files(dry_run=True)
        cleanup_preview = self.cleanup_old_files(dry_run=True)
        alerts = self.check_alerts(disk_info, memory_info)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "disk_usage": disk_info,
            "memory_usage": memory_info,
            "file_usage": file_info,
            "compression_opportunities": compression_preview,
            "cleanup_opportunities": cleanup_preview,
            "alerts": alerts,
            "summary": self._generate_summary(disk_info, memory_info, file_info, alerts)
        }
        
        return report
        
    def _generate_summary(self, disk_info, memory_info, file_info, alerts):
        """Generate summary statistics"""
        summary = {
            "overall_status": "OK",
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a['level'] == 'CRITICAL']),
            "warning_alerts": len([a for a in alerts if a['level'] == 'WARNING'])
        }
        
        if summary['critical_alerts'] > 0:
            summary['overall_status'] = "CRITICAL"
        elif summary['warning_alerts'] > 0:
            summary['overall_status'] = "WARNING"
            
        if disk_info:
            summary['disk_usage_gb'] = disk_info['used_gb']
            summary['disk_free_gb'] = disk_info['free_gb']
            
        if memory_info and memory_info['pipeline_processes']:
            summary['pipeline_memory_mb'] = sum(p['memory_mb'] for p in memory_info['pipeline_processes'])
            
        if file_info:
            summary['total_pipeline_data_gb'] = file_info['total_size_gb']
            
        return summary
        
    def perform_maintenance(self, compress=True, cleanup=False):
        """Perform maintenance operations"""
        results = {
            "compression": None,
            "cleanup": None,
            "errors": []
        }
        
        if compress:
            self.logger.info("Starting file compression...")
            results['compression'] = self.compress_old_files(dry_run=False)
            
        if cleanup:
            self.logger.info("Starting file cleanup...")
            results['cleanup'] = self.cleanup_old_files(dry_run=False)
            
        return results

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline Resource Monitor")
    parser.add_argument('--report', action='store_true', help='Generate resource report')
    parser.add_argument('--compress', action='store_true', help='Compress old files')
    parser.add_argument('--cleanup', action='store_true', help='Delete very old files')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--watch', type=int, metavar='SECONDS', help='Monitor continuously')
    
    args = parser.parse_args()
    
    monitor = ResourceMonitor()
    
    if args.watch:
        # Continuous monitoring
        import time
        print(f"Starting continuous monitoring (every {args.watch} seconds)...")
        try:
            while True:
                report = monitor.generate_report()
                if args.json:
                    print(json.dumps(report, indent=2))
                else:
                    print_report_summary(report)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            
    elif args.compress or args.cleanup:
        # Maintenance mode
        results = monitor.perform_maintenance(compress=args.compress, cleanup=args.cleanup)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_maintenance_results(results)
            
    else:
        # Single report
        report = monitor.generate_report()
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report_summary(report)

def print_report_summary(report):
    """Print human-readable report summary"""
    print("\n" + "="*80)
    print("           PIPELINE RESOURCE USAGE REPORT")
    print("="*80)
    
    summary = report['summary']
    print(f"Overall Status: {summary['overall_status']}")
    print(f"Timestamp: {report['timestamp']}")
    
    if report['alerts']:
        print(f"\n🚨 ALERTS ({len(report['alerts'])}):")
        for alert in report['alerts']:
            print(f"  {alert['level']}: {alert['message']}")
    
    # Disk usage
    if report['disk_usage']:
        disk = report['disk_usage']
        print(f"\n💾 DISK USAGE:")
        print(f"  Used: {disk['used_gb']}GB ({disk['used_percent']}%)")
        print(f"  Free: {disk['free_gb']}GB")
        print(f"  Status: {disk['status']}")
    
    # Memory usage
    if report['memory_usage']:
        memory = report['memory_usage']
        print(f"\n🧠 MEMORY USAGE:")
        print(f"  System: {memory['system']['used_percent']}% ({memory['system']['used_gb']}GB)")
        if memory['pipeline_processes']:
            for proc in memory['pipeline_processes']:
                print(f"  Pipeline PID {proc['pid']}: {proc['memory_mb']}MB ({proc['memory_percent']}%)")
    
    # File usage
    if report['file_usage']:
        files = report['file_usage']
        print(f"\n📁 FILE USAGE:")
        print(f"  Total pipeline data: {files['total_size_gb']}GB")
        for category, info in files['categories'].items():
            if info['file_count'] > 0:
                print(f"  {category}: {info['file_count']} files, {info['total_size_mb']}MB")
    
    # Maintenance opportunities
    compression = report.get('compression_opportunities', {})
    if compression.get('compressed_files'):
        print(f"\n🗜️  COMPRESSION OPPORTUNITIES:")
        print(f"  {len(compression['compressed_files'])} files can be compressed")
        
    cleanup = report.get('cleanup_opportunities', {})
    if cleanup.get('deleted_files'):
        print(f"\n🗑️  CLEANUP OPPORTUNITIES:")
        print(f"  {len(cleanup['deleted_files'])} files can be deleted")
    
    print("="*80)

def print_maintenance_results(results):
    """Print maintenance operation results"""
    print("\n" + "="*60)
    print("         MAINTENANCE RESULTS")
    print("="*60)
    
    if results['compression']:
        comp = results['compression']
        print(f"\n🗜️  COMPRESSION:")
        print(f"  Files processed: {len(comp['compressed_files'])}")
        if comp['errors']:
            print(f"  Errors: {len(comp['errors'])}")
            for error in comp['errors']:
                print(f"    - {error}")
                
    if results['cleanup']:
        clean = results['cleanup']
        print(f"\n🗑️  CLEANUP:")
        print(f"  Files processed: {len(clean['deleted_files'])}")
        if clean['errors']:
            print(f"  Errors: {len(clean['errors'])}")
            for error in clean['errors']:
                print(f"    - {error}")
    
    print("="*60)

if __name__ == "__main__":
    main()