#!/bin/bash
DEST=container/runner FLAG=$1 make
DEST=src/bpf_loader FLAG=SSM{fake_flag_here} make
