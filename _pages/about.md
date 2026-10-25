---
layout: about
title: about
permalink: /
# The subtitle (headline) and the line under the photo (location) come from content/profile.yml.

profile:
  align: right
  image: prof_pic.jpg # symlink to content/photo.jpg
  image_circular: false

selected_papers: true # papers marked `selected = {true}` in content/papers.bib
social: true # contact icons from content/profile.yml

announcements:
  enabled: false
latest_posts:
  enabled: false
---

{{ site.data.profile.bio | markdownify }}
