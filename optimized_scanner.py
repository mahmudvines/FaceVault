"""
Optimized Face Scanning with Multiprocessing and Batching
Dramatically faster scanning for large photo collections
"""

import os
import json
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count
import face_recognition


def process_single_image(args):
    """Process a single image - used for multiprocessing"""
    img_path, model = args
    try:
        image = face_recognition.load_image_file(img_path)
        locations = face_recognition.face_locations(image, model=model)
        encodings = face_recognition.face_encodings(image, locations)
        
        if encodings:
            return {
                'path': img_path,
                'encodings': [enc.tolist() for enc in encodings],
                'status': 'found'
            }
        else:
            return {
                'path': img_path,
                'status': 'no_face'
            }
    except Exception as e:
        return {
            'path': img_path,
            'status': 'error',
            'error': str(e)
        }


class OptimizedScanner:
    """Optimized face scanning with batch processing and multiprocessing"""
    
    def __init__(self, tolerance=0.50, model='hog', num_processes=None):
        """
        Initialize scanner
        
        Args:
            tolerance: Face recognition tolerance (0-1)
            model: 'hog' (faster) or 'cnn' (more accurate)
            num_processes: Number of parallel workers (default: CPU count - 1)
        """
        self.tolerance = tolerance
        self.model = model
        self.num_processes = num_processes or max(1, cpu_count() - 1)
        
        # Cache for known encodings (numpy arrays for fast comparison)
        self.cluster_cache = {}
    
    def find_images(self, folder, extensions=None):
        """Find all image files in folder"""
        if extensions is None:
            extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        
        images = []
        try:
            for p in Path(folder).rglob("*"):
                if p.suffix.lower() in extensions and p.is_file():
                    images.append(str(p))
        except PermissionError:
            pass
        
        return images
    
    def scan_folder(self, folder, db, processed_set=None):
        """
        Scan folder for faces - optimized version
        
        Returns: (added, no_face_list)
        """
        if processed_set is None:
            processed_set = set()
        
        # Find new images
        all_images = self.find_images(folder)
        new_images = [img for img in all_images if img not in processed_set]
        
        if not new_images:
            print(f"[Scanner] No new images to process in {folder}")
            return 0, []
        
        # Process images in parallel
        print(f"[Scanner] Processing {len(new_images)} images with {self.num_processes} workers...")
        
        try:
            image_results = self._process_images_parallel(new_images)
            print(f"[Scanner] Image processing complete. Got {len(image_results)} results")
        except Exception as e:
            print(f"[Scanner ERROR] Failed to process images: {type(e).__name__}: {str(e)}")
            raise
        
        # Update database with results
        added = 0
        no_face = []
        errors = []
        
        for result in image_results:
            try:
                if result['status'] == 'found':
                    enc_count = self._add_encodings_to_db(result['path'], result['encodings'], db)
                    added += enc_count
                    processed_set.add(result['path'])
                    print(f"[Scanner] Added {enc_count} face(s) from {os.path.basename(result['path'])}")
                elif result['status'] == 'no_face':
                    no_face.append(result['path'])
                    processed_set.add(result['path'])
                elif result['status'] == 'error':
                    errors.append((result['path'], result.get('error', 'Unknown error')))
                    processed_set.add(result['path'])
                    print(f"[Scanner] Error processing {os.path.basename(result['path'])}: {result.get('error')}")
            except Exception as e:
                print(f"[Scanner ERROR] Failed to process result: {type(e).__name__}: {str(e)}")
                errors.append((result.get('path', 'unknown'), str(e)))
                processed_set.add(result.get('path', ''))
        
        print(f"[Scanner] Complete: {added} faces added, {len(no_face)} no-face, {len(errors)} errors")
        return added, no_face
    
    def _process_images_parallel(self, image_paths):
        """Process images in parallel using multiprocessing"""
        # Create task list
        tasks = [(path, self.model) for path in image_paths]
        
        results = []
        with Pool(self.num_processes) as pool:
            for result in pool.imap_unordered(process_single_image, tasks, chunksize=4):
                results.append(result)
        
        return results
    
    def _add_encodings_to_db(self, img_path, encodings, db):
        """Add encodings to database clusters"""
        added = 0
        
        for enc in encodings:
            enc_array = np.array(enc)
            matched = False
            
            # Try to match with existing cluster
            for cluster in db["clusters"]:
                if self._matches_cluster(enc_array, cluster):
                    cluster["photos"].append(img_path)
                    cluster["encodings"].append(enc)
                    matched = True
                    break
            
            # Create new cluster if no match
            if not matched:
                db["clusters"].append({
                    "id": db["next_id"],
                    "name": "",
                    "photos": [img_path],
                    "encodings": [enc]
                })
                db["next_id"] += 1
            
            added += 1
        
        return added
    
    def _matches_cluster(self, enc_array, cluster):
        """Fast cluster matching using vectorized comparison"""
        if not cluster.get("encodings"):
            return False
        
        # Convert all cluster encodings at once (vectorized)
        known = np.array(cluster.get("encodings", []))
        
        if len(known.shape) == 1:  # Single encoding
            known = known.reshape(1, -1)
        
        # Vectorized distance calculation
        distances = np.linalg.norm(known - enc_array, axis=1)
        
        # Check if any distance is below tolerance
        return np.any(distances < (1.0 - self.tolerance))


def get_optimized_scanner(tolerance=0.50, use_cnn=False):
    """Get configured scanner instance"""
    model = 'cnn' if use_cnn else 'hog'  # CNN slower but more accurate
    return OptimizedScanner(tolerance=tolerance, model=model)
