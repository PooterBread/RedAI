"""
Udoo Key Optimized Version
Lightweight version optimized for Udoo Key's resource constraints
"""

import sys
import gc
from micropython_compat import IS_MICROPYTHON

class UdooKeyOptimizer:
    """Optimizations for Udoo Key hardware constraints"""
    
    def __init__(self):
        self.memory_threshold = 100000  # 100KB threshold for garbage collection
        
    def optimize_memory(self):
        """Force garbage collection on memory-constrained devices"""
        if IS_MICROPYTHON:
            gc.collect()
    
    def check_memory(self):
        """Check available memory (MicroPython only)"""
        if IS_MICROPYTHON:
            try:
                import gc
                free_mem = gc.mem_free()
                return free_mem
            except:
                return None
        return None
    
    def should_optimize(self):
        """Determine if optimization is needed"""
        if IS_MICROPYTHON:
            free = self.check_memory()
            if free and free < self.memory_threshold:
                return True
        return False

def optimize_for_udoo_key(func):
    """Decorator to optimize functions for Udoo Key"""
    def wrapper(*args, **kwargs):
        optimizer = UdooKeyOptimizer()
        if optimizer.should_optimize():
            optimizer.optimize_memory()
        result = func(*args, **kwargs)
        if IS_MICROPYTHON:
            optimizer.optimize_memory()
        return result
    return wrapper







