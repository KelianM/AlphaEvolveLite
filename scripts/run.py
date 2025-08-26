#!/usr/bin/env python
"""
CLI entry-point.
Run: python scripts/run.py path/to/config.yml [--debug] [--resume]
"""
import sys
import argparse
from alphaevolve.config import Config
from alphaevolve.controller import EvolutionController

def main():
    parser = argparse.ArgumentParser(description='Run AlphaEvolve evolution experiment')
    parser.add_argument('config', help='Path to configuration YAML file')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug logging (verbose individual-level output)')
    parser.add_argument('--resume', action='store_true',
                       help='Resume evolution from the current generation in the database')
    parser.add_argument('--workers', type=int, default=None,
                       help='Number of workers for the controller threadpool (overrides config file)')
    
    args = parser.parse_args()
    
    # Load config
    cfg = Config.load(args.config)
    
    # Override debug setting from command line
    cfg.debug = args.debug
    
    # Override max_workers setting from command line if specified
    if args.workers is not None:
        cfg.evolution.max_workers = args.workers
    
    # Run evolution
    EvolutionController(cfg, resume=args.resume).run_evolution()

if __name__ == "__main__":
    main()