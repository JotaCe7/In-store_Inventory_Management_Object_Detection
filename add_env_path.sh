#!/bin/sh

set -e

# Auto-Get the latest commit sha via command line.
get_latest_release() {
    tag=$(curl --silent "https://api.github.com/repos/${1}/releases/latest" | # Get latest release from GitHub API
          grep '"tag_name":'                                              | # Get tag line
          sed -E 's/.*"([^"]+)".*/\1/'                                    ) # Pluck JSON value

    tag_data=$(curl --silent "https://api.github.com/repos/${1}/git/ref/tags/${tag}")

    sha=$(echo "${tag_data}"           | # Get latest release from GitHub API
          grep '"sha":'                | # Get tag line
          sed -E 's/.*"([^"]+)".*/\1/' ) # Pluck JSON value

    sha_type=$(echo "${tag_data}"           | # Get latest release from GitHub API
          grep '"type":'                    | # Get tag line
          sed -E 's/.*"([^"]+)".*/\1/'      ) # Pluck JSON value

    if [ "${sha_type}" != "commit" ]; then
        combo_sha=$(curl -s "https://api.github.com/repos/${1}/git/tags/${sha}" | # Get latest release from GitHub API
              grep '"sha":'                                                     | # Get tag line
              sed -E 's/.*"([^"]+)".*/\1/'                                      ) # Pluck JSON value

        # Remove the tag sha, leaving only the commit sha;
        # this won't work if there are ever more than 2 sha,
        # and use xargs to remove whitespace/newline.
        sha=$(echo "${combo_sha}" | sed -E "s/${sha}//" | xargs)
    fi

    printf "${sha}"
}

ARCH="x64"
U_NAME=$(uname -m)

if [ "${U_NAME}" = "aarch64" ]; then
    ARCH="arm64"
fi

archive="vscode-server-linux-${ARCH}.tar.gz"
owner='microsoft'
repo='vscode'
commit_sha=$(get_latest_release "${owner}/${repo}")

# Add code-server to $PATH
export PATH="$PATH:/home/app/.vscode-server/bin/${commit_sha}/bin"

# Here can be added aditional visual studio code extensions
#code-server --install-extension your-extension-eg-ms-python.python