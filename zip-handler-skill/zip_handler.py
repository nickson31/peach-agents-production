#!/usr/bin/env python3
"""
ZIP Handler - Manage ZIP files
Extract, create, inspect, validate, and merge ZIP archives
"""

import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import sys

class ZipHandler:
    """Handle ZIP file operations"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
    
    def log(self, msg: str):
        if self.verbose:
            print(f"[ZIP] {msg}")
    
    # =========================================================================
    # EXTRACT
    # =========================================================================
    
    def extract_zip(self, 
                   zip_path: str, 
                   extract_to: Optional[str] = None,
                   password: Optional[str] = None) -> bool:
        """
        Extract ZIP file to specified directory
        
        Args:
            zip_path: Path to ZIP file
            extract_to: Destination directory (default: same as zip name)
            password: Password for encrypted ZIP (if any)
        
        Returns:
            True if successful
        """
        
        zip_path = Path(zip_path)
        if not zip_path.exists():
            self.log(f"❌ ZIP not found: {zip_path}")
            return False
        
        if not extract_to:
            extract_to = zip_path.stem
        
        extract_to = Path(extract_to)
        extract_to.mkdir(parents=True, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                if password:
                    zf.setpassword(password.encode())
                
                zf.extractall(extract_to)
            
            self.log(f"✅ Extracted to: {extract_to}")
            return True
        
        except Exception as e:
            self.log(f"❌ Extract failed: {e}")
            return False
    
    # =========================================================================
    # CREATE
    # =========================================================================
    
    def create_zip(self,
                  source_path: str,
                  zip_name: str,
                  compression: str = 'default') -> bool:
        """
        Create ZIP archive from file or folder
        
        Args:
            source_path: File or folder to zip
            zip_name: Output ZIP filename
            compression: 'fastest', 'default', or 'best'
        
        Returns:
            True if successful
        """
        
        source_path = Path(source_path)
        if not source_path.exists():
            self.log(f"❌ Source not found: {source_path}")
            return False
        
        # Map compression levels
        compression_map = {
            'fastest': zipfile.ZIP_DEFLATED,
            'default': zipfile.ZIP_DEFLATED,
            'best': zipfile.ZIP_DEFLATED
        }
        compress_type = compression_map.get(compression, zipfile.ZIP_DEFLATED)
        
        try:
            with zipfile.ZipFile(zip_name, 'w', compress_type) as zf:
                if source_path.is_file():
                    zf.write(source_path, arcname=source_path.name)
                else:
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path.parent)
                            zf.write(file_path, arcname=arcname)
            
            size = Path(zip_name).stat().st_size / (1024*1024)
            self.log(f"✅ Created: {zip_name} ({size:.2f} MB)")
            return True
        
        except Exception as e:
            self.log(f"❌ Create failed: {e}")
            return False
    
    # =========================================================================
    # INSPECT
    # =========================================================================
    
    def inspect_zip(self, zip_path: str) -> Optional[Dict]:
        """
        List and analyze ZIP contents
        
        Returns:
            Dict with {files, total_size, compressed_size, ratio, file_list}
        """
        
        zip_path = Path(zip_path)
        if not zip_path.exists():
            self.log(f"❌ ZIP not found: {zip_path}")
            return None
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                file_list = zf.namelist()
                total_size = sum(zf.getinfo(f).file_size for f in file_list)
                compressed_size = sum(zf.getinfo(f).compress_size for f in file_list)
                
                ratio = (1 - compressed_size/total_size)*100 if total_size > 0 else 0
                
                info = {
                    'files': len(file_list),
                    'total_size': total_size,
                    'compressed_size': compressed_size,
                    'ratio': ratio,
                    'file_list': file_list[:20]  # First 20 files
                }
                
                self.log(f"📊 Zip contents:")
                self.log(f"   Files: {len(file_list)}")
                self.log(f"   Total: {total_size/(1024*1024):.2f} MB")
                self.log(f"   Compressed: {compressed_size/(1024*1024):.2f} MB")
                self.log(f"   Ratio: {ratio:.1f}%")
                
                return info
        
        except Exception as e:
            self.log(f"❌ Inspect failed: {e}")
            return None
    
    # =========================================================================
    # VALIDATE
    # =========================================================================
    
    def validate_zip(self, zip_path: str) -> bool:
        """
        Check ZIP integrity
        
        Returns:
            True if valid, False if corrupted
        """
        
        zip_path = Path(zip_path)
        if not zip_path.exists():
            self.log(f"❌ ZIP not found: {zip_path}")
            return False
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                result = zf.testzip()
                if result is None:
                    self.log(f"✅ ZIP is valid")
                    return True
                else:
                    self.log(f"❌ Corrupted: {result}")
                    return False
        
        except Exception as e:
            self.log(f"❌ Validation failed: {e}")
            return False
    
    # =========================================================================
    # MERGE
    # =========================================================================
    
    def merge_zips(self,
                  zip_list: List[str],
                  output_name: str) -> bool:
        """
        Combine multiple ZIPs into one
        
        Args:
            zip_list: List of ZIP files to merge
            output_name: Output merged ZIP filename
        
        Returns:
            True if successful
        """
        
        try:
            with zipfile.ZipFile(output_name, 'w') as out_zf:
                for zip_file in zip_list:
                    with zipfile.ZipFile(zip_file, 'r') as zf:
                        for item in zf.infolist():
                            data = zf.read(item.filename)
                            out_zf.writestr(item, data)
            
            size = Path(output_name).stat().st_size / (1024*1024)
            self.log(f"✅ Merged {len(zip_list)} ZIPs → {output_name} ({size:.2f} MB)")
            return True
        
        except Exception as e:
            self.log(f"❌ Merge failed: {e}")
            return False


# ============================================================================
# CLI
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='ZIP Handler')
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Extract
    extract_parser = subparsers.add_parser('extract', help='Extract ZIP')
    extract_parser.add_argument('zip_file', help='ZIP file')
    extract_parser.add_argument('-o', '--output', help='Output directory')
    extract_parser.add_argument('-p', '--password', help='Password')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create ZIP')
    create_parser.add_argument('source', help='Source file/folder')
    create_parser.add_argument('-n', '--name', required=True, help='ZIP name')
    create_parser.add_argument('-c', '--compression', default='default')
    
    # Inspect
    inspect_parser = subparsers.add_parser('inspect', help='Inspect ZIP')
    inspect_parser.add_argument('zip_file', help='ZIP file')
    
    # Validate
    validate_parser = subparsers.add_parser('validate', help='Validate ZIP')
    validate_parser.add_argument('zip_file', help='ZIP file')
    
    # Merge
    merge_parser = subparsers.add_parser('merge', help='Merge ZIPs')
    merge_parser.add_argument('zip_files', nargs='+', help='ZIP files')
    merge_parser.add_argument('-o', '--output', required=True, help='Output ZIP')
    
    args = parser.parse_args()
    handler = ZipHandler()
    
    if args.command == 'extract':
        handler.extract_zip(args.zip_file, args.output, args.password)
    elif args.command == 'create':
        handler.create_zip(args.source, args.name, args.compression)
    elif args.command == 'inspect':
        handler.inspect_zip(args.zip_file)
    elif args.command == 'validate':
        handler.validate_zip(args.zip_file)
    elif args.command == 'merge':
        handler.merge_zips(args.zip_files, args.output)
    else:
        parser.print_help()
