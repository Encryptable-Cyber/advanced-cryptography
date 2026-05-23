#!/bin/bash
# Hash Benchmark Script - Compare MD5 vs SHA-256 performance

echo "=========================================="
echo "Hash Benchmark: MD5 vs SHA-256"
echo "=========================================="
echo ""

# Create a test file of random data (10MB instead of 100MB for speed)
echo "Creating 10MB test file..."
dd if=/dev/urandom of=testfile.bin bs=1M count=10 2>/dev/null
echo ""

# Test MD5 performance
echo "Testing MD5 performance..."
START_TIME=$(date +%s.%N)
for i in {1..100}; do
    md5sum testfile.bin > /dev/null 2>&1
done
END_TIME=$(date +%s.%N)
MD5_TIME=$(echo "$END_TIME - $START_TIME" | bc)
echo "MD5: 100 hashes completed in ${MD5_TIME} seconds"
echo ""

# Test SHA-256 performance
echo "Testing SHA-256 performance..."
START_TIME=$(date +%s.%N)
for i in {1..100}; do
    sha256sum testfile.bin > /dev/null 2>&1
done
END_TIME=$(date +%s.%N)
SHA256_TIME=$(echo "$END_TIME - $START_TIME" | bc)
echo "SHA-256: 100 hashes completed in ${SHA256_TIME} seconds"
echo ""

# Calculate and display ratio
echo "=========================================="
RATIO=$(echo "scale=2; $SHA256_TIME / $MD5_TIME" | bc)
echo "Speed Ratio: MD5 is ${RATIO}x faster than SHA-256"
echo "=========================================="

# Clean up
rm testfile.bin
