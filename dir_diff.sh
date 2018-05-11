#!/bin/bash
vimdiff <(cd $1; find . | sort) <(cd $2; find . | sort)
