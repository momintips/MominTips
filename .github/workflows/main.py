name: generate tetris animation

on:
  # run automatically every 24 hours
  schedule:
    - cron: "0 */24 * * *"
  
  # allows to manually run the job at any time
  workflow_dispatch:
  
  # run on every push on the master branch
  push:
    branches:
    - main

jobs:
  generate:
    permissions: 
      contents: write
    runs-on: ubuntu-latest
    timeout-minutes: 5
    
    steps:
      # generates a tetris game from github contributions
      - name: generate github-contribution-tetris.svg
        uses: marcodavi/snk-tetris@main
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-contribution-tetris.svg
            dist/github-contribution-tetris-dark.svg?palette=github-dark
          
      # push the generated files to output branch
      - name: push tetris animation to the output branch
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}