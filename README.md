# esjob-script

Scripts for Elastic-Job.

`job-switch.py`:

- Supported version: `com.dangdang.elastic-job@2.1.5`
- Usage: Enable / disable all elastic jobs by modifying nodes in zookeeper. This script won't affect jobs that are already running, disabling jobs only prevent them to start.