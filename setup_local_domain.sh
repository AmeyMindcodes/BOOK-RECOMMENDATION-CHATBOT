#!/bin/bash

# This script adds bookbot.ai to your hosts file
# Run with sudo on macOS/Linux: sudo ./setup_local_domain.sh

# Check if running as root/admin
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root/administrator (use sudo)"
  exit 1
fi

# Add entry to hosts file
echo "Adding bookbot.ai to hosts file..."
echo "127.0.0.1 bookbot.ai" >> /etc/hosts

echo "Done! You can now access your app at http://bookbot.ai:5000"
echo "To remove this entry later, edit /etc/hosts and remove the line with bookbot.ai" 