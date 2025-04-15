#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ví dụ sử dụng Vietnamese Corpus Filter
"""

import os
import logging
from vietnamese_corpus_filter import filter_corpus

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Hàm chính để chạy ví dụ
    """
    input_file = "corpus_sample.txt"
    output_file = "corpus_sample_filtered_example.txt"
    
    if not os.path.exists(input_file):
        logger.error(f"File đầu vào không tồn tại: {input_file}")
        return 1
    
    logger.info(f"Bắt đầu lọc file: {input_file}")
    filter_corpus(input_file, output_file)
    logger.info(f"Hoàn thành. Kết quả đã được ghi vào: {output_file}")
    
    return 0

if __name__ == "__main__":
    exit(main())