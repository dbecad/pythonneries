# Environment build
## SSH key creation, add to github & test
[Github details](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

Create a public SSH key `ssh-keygen -t ed25519 -C "your_email@example.com"`

Cat the content `cat ~/.ssh/id_***.pub` and copy it in the github config (Settings/SSH keys/New SSH key) then test it with `ssh -T git@github.com`

## Clone repo and set Users
Now repositories should be SSH clonable `git clone git@github.com:dbecad/****.git`

In the repo
`git config user.name "dbe cad" && git config user.email "damien.job@gmail.com" && cat .git/config`

## Poetry
