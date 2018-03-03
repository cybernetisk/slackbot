#!/bin/bash

#Exit the script if you get any errors

set -e

if [ ! -z "$TRAVIS" ]; then
  echo "Decrypting ssh-key and adding"
  openssl aes-256-cbc -K $encrypted_b3a9f4cfdc6e_key -iv $encrypted_b3a9f4cfdc6e_iv -in travis.enc -out travis -d
  chmod 600 travis
  eval "$(ssh-agent)"
  ssh-add travis
fi

echo "Running remote SSH-script"
ssh -o StrictHostKeyChecking=no root@slackbot.cyb.no /bin/bash << EOF
  set -e
  cd ~/drift/slackbot
  ./update.sh
EOF

echo "Deploy finished"
