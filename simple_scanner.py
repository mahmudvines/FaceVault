"""
Simple, reliable face scanning without multiprocessing
Fast enough and never hangs
"""

import os
import numpy as np
from pathlib import Path
import face_recognition


class SimpleScanner:
    """Simple sequential face scanning - reliable and never hangs"""
    
    def __init__(self, tolerance=0.50, model='hog'):
        """
        Initialize scanner
        
        Args:
            tolerance: Face recognition tolerance (0-1)
            model: 'hog' (faster) or 'cnn' (more accurate)
        """
        self.tolerance = tolerance
        self.model = model
    
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
        Scan folder for faces - simple sequential version
        
        Returns: (added, no_face_list)
        """
        if processed_set is None:
            processed_set = set()
        
        # Find new images
        all_images = self.find_images(folder)
        new_images = [img for img in all_images if img not in processed_set]
        
        if not new_images:
            print(f"[SimpleScanner] No new images to process")
            return 0, []
        
        print(f"[SimpleScanner] Processing {len(new_images)} images sequentially...")
        
        added = 0
        no_face = []
        errors = []
        
        for idx, img_path in enumerate(new_images, 1):
            try:
                # Log progress every 10 images
                if idx % 10 == 0 or idx == 1:
                    print(f"[SimpleScanner] Progress: {idx}/{len(new_images)} images")
                
                image = face_recognition.load_image_file(img_path)
                locations = face_recognition.face_locations(image, model=self.model)
                encodings = face_recognition.face_encodings(image, locations)
                
                if not encodings:
                    no_face.append(img_path)
                    processed_set.add(img_path)
                    continue
                
                # Add encodings to database
                for enc in encodings:
                    enc_array = np.array(enc)
                    matched = False
                    
                    # Try to match with existing cluster
                    for cluster in db.get("clusters", []):
                        if self._matches_cluster(enc_array, cluster):
                            cluster["photos"].append(img_path)
                            cluster["encodings"].append(enc.tolist())
                            matched = True
                            break
                    
                    # Create new cluster if no match
                    if not matched:
                        db.setdefault("clusters", []).append({
                            "id": db.get("next_id", 1),
                            "name": "",
                            "photos": [img_path],
                            "encodings": [enc.tolist()]
                        })
                        db["next_id"] = db.get("next_id", 1) + 1
                    
                    added += 1
                
                processed_set.add(img_path)
                
            except Exception as e:
                print(f"[SimpleScanner] Error processing {os.path.basename(img_path)}: {str(e)}")
                errors.append((img_path, str(e)))
                processed_set.add(img_path)
        
        print(f"[SimpleScanner] Complete: {added} faces added, {len(no_face)} no-face, {len(errors)} errors")
        return added, no_face
    
    def _matches_cluster(self, enc_array, cluster):
        """Check if encoding matches cluster"""
        if not cluster.get("encodings"):
            return False
        
        # Convert cluster encodings to array
        known = np.array(cluster.get("encodings", []))
        
        if len(known.shape) == 1:
            known = known.reshape(1, -1)
        
        # Fast distance calculation
        distances = np.linalg.norm(known - enc_array, axis=1)
        
        # Check if any distance is below tolerance
        return np.any(distances < (1.0 - self.tolerance))


def get_simple_scanner(tolerance=0.50, use_cnn=False):
    """Get configured simple scanner instance"""
    model = 'cnn' if use_cnn else 'hog'
    return SimpleScanner(tolerance=tolerance, model=model)
