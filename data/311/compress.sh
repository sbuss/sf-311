#!/bin/bash
tar cz 311_Cases.tsv 311_Cases.pickle | split -b 50MiB - cases.tgz_
