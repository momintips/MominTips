name: generate flower animation

on:
  schedule:
    - cron: "0 */24 * * *"
  workflow_dispatch:
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
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Generate flower animation
        uses: actions/python@v4
        with:
          python-version: '3.10'
          script: |
            import requests
            from datetime import datetime, timedelta
            import svgwrite
            
            # Get contribution data
            username = "${{ github.repository_owner }}"
            url = f"https://github.com/users/{username}/contributions"
            response = requests.get(url)
            data = response.text
            
            # Parse contributions (simplified example)
            contributions = []
            for line in data.split('\n'):
                if 'data-count=' in line:
                    count = int(line.split('data-count="')[1].split('"')[0])
                    date = line.split('data-date="')[1].split('"')[0]
                    contributions.append((date, count))
            
            # Create SVG
            dwg = svgwrite.Drawing('dist/github-contribution-flower.svg', size=('800', '600'))
            
            # Draw flower based on contributions
            center_x, center_y = 400, 300
            max_petals = max(1, sum(c[1] for c in contributions[-30:]))  # Last 30 days
            
            # Stem
            dwg.add(dwg.line(start=(center_x, center_y+100), 
                            end=(center_x, center_y+200), 
                            stroke='#2cbe4e', 
                            stroke_width=10))
            
            # Center
            dwg.add(dwg.circle(center=(center_x, center_y), 
                              r=max_petals/2, 
                              fill='#f9d71c'))
            
            # Petals (one per contribution)
            for i, (date, count) in enumerate(contributions[-30:]):
                if count > 0:
                    angle = (i * 360/30) * 3.14159/180
                    length = 30 + min(count, 10) * 5
                    end_x = center_x + length * math.cos(angle)
                    end_y = center_y + length * math.sin(angle)
                    
                    dwg.add(dwg.line(start=(center_x, center_y), 
                                    end=(end_x, end_y), 
                                    stroke='#ff6b6b', 
                                    stroke_width=3+count/2))
            
            # Add text
            dwg.add(dwg.text(f"{username}'s Contribution Flower", 
                            insert=(center_x, center_y+250), 
                            font_size=20, 
                            text_anchor='middle',
                            fill='#333'))
            
            dwg.save()
            
      - name: Push flower animation to output branch
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}