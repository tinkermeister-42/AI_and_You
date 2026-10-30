-- ytvideo.lua: {{< ytvideo VIDEO_ID title="..." >}}
-- Embeds a YouTube video from youtube-nocookie.com (privacy mode, for home)
-- and adds a link to the same video on yout-ube.com, which students can open
-- at school: the school blocks youtube.com and youtube-nocookie.com, but not
-- yout-ube.com, and it needs no login (October 2026). Quarto's own video
-- shortcode rewrites every YouTube address to youtube.com, so it can't be used.
return {
  ['ytvideo'] = function(args, kwargs)
    local id = pandoc.utils.stringify(args[1])
    local title = pandoc.utils.stringify(kwargs["title"] or "Video")
    title = title:gsub('"', "&quot;")
    local html = '<div class="quarto-video ratio ratio-16x9"><iframe src="https://www.youtube-nocookie.com/embed/' .. id ..
      '" title="' .. title .. '" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' ..
      'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>' ..
      '<p class="yt-school">🏫 <strong>At school:</strong> <a href="https://yout-ube.com/watch?v=' .. id ..
      '" target="_blank" rel="noopener">watch this video on yout-ube.com</a></p>'
    return pandoc.RawBlock("html", html)
  end
}
