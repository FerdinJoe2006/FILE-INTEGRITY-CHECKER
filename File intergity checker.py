import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path

class FileIntegrityMonitor:
    def __init__(self, db_file="integrity_database.json"):
        self.db_file = db_file
        self.file_records = self.load_database()
    
    def calculate_hash(self, filepath, algorithm='sha256'):
        """Calculate hash value for a given file"""
        hash_func = hashlib.new(algorithm)
        
        try:
            with open(filepath, 'rb') as f:
                # Read file in chunks to handle large files efficiently
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found")
            return None
        except PermissionError:
            print(f"Error: Permission denied for '{filepath}'")
            return None
        except Exception as e:
            print(f"Error processing '{filepath}': {str(e)}")
            return None
    
    def load_database(self):
        """Load existing file records from database"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Database file corrupted. Starting fresh.")
                return {}
        return {}
    
    def save_database(self):
        """Save file records to database"""
        with open(self.db_file, 'w') as f:
            json.dump(self.file_records, f, indent=4)
    
    def register_file(self, filepath):
        """Register a new file for monitoring"""
        if not os.path.exists(filepath):
            print(f"File '{filepath}' does not exist")
            return False
        
        abs_path = os.path.abspath(filepath)
        file_hash = self.calculate_hash(abs_path)
        
        if file_hash:
            file_size = os.path.getsize(abs_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.file_records[abs_path] = {
                'hash': file_hash,
                'size': file_size,
                'registered': timestamp,
                'last_checked': timestamp,
                'status': 'intact'
            }
            
            self.save_database()
            print(f"✓ File registered: {filepath}")
            print(f"  Hash: {file_hash}")
            return True
        
        return False
    
    def check_file(self, filepath):
        """Check if a file has been modified"""
        abs_path = os.path.abspath(filepath)
        
        if abs_path not in self.file_records:
            print(f"File '{filepath}' is not registered for monitoring")
            return None
        
        if not os.path.exists(abs_path):
            print(f"⚠ WARNING: File '{filepath}' has been deleted!")
            self.file_records[abs_path]['status'] = 'deleted'
            self.save_database()
            return False
        
        current_hash = self.calculate_hash(abs_path)
        stored_hash = self.file_records[abs_path]['hash']
        current_size = os.path.getsize(abs_path)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file_records[abs_path]['last_checked'] = timestamp
        
        if current_hash == stored_hash:
            print(f"✓ File intact: {filepath}")
            self.file_records[abs_path]['status'] = 'intact'
            self.save_database()
            return True
        else:
            print(f"⚠ ALERT: File modified: {filepath}")
            print(f"  Original hash: {stored_hash}")
            print(f"  Current hash:  {current_hash}")
            print(f"  Size change: {self.file_records[abs_path]['size']} → {current_size} bytes")
            
            self.file_records[abs_path]['status'] = 'modified'
            self.save_database()
            return False
    
    def check_all_files(self):
        """Check integrity of all registered files"""
        print("\n" + "="*60)
        print("FILE INTEGRITY CHECK - FULL SCAN")
        print("="*60)
        
        if not self.file_records:
            print("No files registered for monitoring")
            return
        
        intact_count = 0
        modified_count = 0
        deleted_count = 0
        
        for filepath in self.file_records.keys():
            result = self.check_file(filepath)
            if result is True:
                intact_count += 1
            elif result is False:
                if self.file_records[filepath]['status'] == 'deleted':
                    deleted_count += 1
                else:
                    modified_count += 1
            print()
        
        print("="*60)
        print(f"Summary: {intact_count} intact | {modified_count} modified | {deleted_count} deleted")
        print("="*60)
    
    def update_baseline(self, filepath):
        """Update the baseline hash for a modified file"""
        abs_path = os.path.abspath(filepath)
        
        if abs_path not in self.file_records:
            print(f"File '{filepath}' is not registered")
            return False
        
        new_hash = self.calculate_hash(abs_path)
        if new_hash:
            self.file_records[abs_path]['hash'] = new_hash
            self.file_records[abs_path]['size'] = os.path.getsize(abs_path)
            self.file_records[abs_path]['status'] = 'intact'
            self.file_records[abs_path]['last_checked'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_database()
            print(f"✓ Baseline updated for: {filepath}")
            return True
        
        return False
    
    def list_monitored_files(self):
        """Display all monitored files and their status"""
        print("\n" + "="*60)
        print("MONITORED FILES")
        print("="*60)
        
        if not self.file_records:
            print("No files registered")
            return
        
        for filepath, info in self.file_records.items():
            status_icon = "✓" if info['status'] == 'intact' else "⚠"
            print(f"\n{status_icon} {filepath}")
            print(f"  Status: {info['status']}")
            print(f"  Hash: {info['hash'][:16]}...")
            print(f"  Registered: {info['registered']}")
            print(f"  Last checked: {info['last_checked']}")
    
    def remove_file(self, filepath):
        """Remove a file from monitoring"""
        abs_path = os.path.abspath(filepath)
        
        if abs_path in self.file_records:
            del self.file_records[abs_path]
            self.save_database()
            print(f"✓ Removed from monitoring: {filepath}")
            return True
        else:
            print(f"File '{filepath}' is not registered")
            return False


def display_menu():
    print("\n" + "="*60)
    print("FILE INTEGRITY CHECKER")
    print("="*60)
    print("1. Register new file for monitoring")
    print("2. Check specific file")
    print("3. Check all monitored files")
    print("4. List all monitored files")
    print("5. Update baseline for modified file")
    print("6. Remove file from monitoring")
    print("7. Exit")
    print("="*60)


def main():
    monitor = FileIntegrityMonitor()
    
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        FILE INTEGRITY CHECKER - CODTECH PROJECT        ║")
    print("║           Secure Your Files with Hash Monitoring       ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            filepath = input("\nEnter file path to register: ").strip()
            monitor.register_file(filepath)
        
        elif choice == '2':
            filepath = input("\nEnter file path to check: ").strip()
            monitor.check_file(filepath)
        
        elif choice == '3':
            monitor.check_all_files()
        
        elif choice == '4':
            monitor.list_monitored_files()
        
        elif choice == '5':
            filepath = input("\nEnter file path to update baseline: ").strip()
            monitor.update_baseline(filepath)
        
        elif choice == '6':
            filepath = input("\nEnter file path to remove: ").strip()
            monitor.remove_file(filepath)
        
        elif choice == '7':
            print("\nThank you for using File Integrity Checker!")
            print("Stay secure! 🔒")
            break
        
        else:
            print("\n⚠ Invalid choice. Please enter a number between 1-7.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
