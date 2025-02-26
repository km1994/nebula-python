# Copyright (c) 2021 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License.

.PHONY: fmt

LINUX_BLACK = ~/.local/bin/black
MAC_BLACK = black
FMT_EXCLUDE = --extend-exclude nebula3/common/\|nebula3/storage/\|nebula3/graph/\|nebula3/meta\|nebula3/common\|nebula3/fbthrift/

fmt:
	pip install --user black
	@if [ -x $(LINUX_BLACK) ];then \
		$(LINUX_BLACK) -S $(FMT_EXCLUDE) .; \
	else \
		$(MAC_BLACK) -S $(FMT_EXCLUDE) .; \
	fi

fmt-check:
	pip install --user black
	@if [ -x $(LINUX_BLACK) ];then \
		$(LINUX_BLACK) -S --check $(FMT_EXCLUDE) .; \
	else \
		$(MAC_BLACK) -S --check $(FMT_EXCLUDE) . ; \
	fi
