-- ytvideo.lua: {{< ytvideo VIDEO_ID title="..." >}}
-- Embeds a YouTube video from youtube-nocookie.com. The school blocks
-- youtube.com for students, but not this domain (October 2026). Quarto's own
-- video shortcode rewrites every YouTube address to youtube.com, so it can't be used.
return {
  ['ytvideo'] = function(args, kwargs)
    local id = pandoc.utils.stringify(args[1])
    local title = pandoc.utils.stringify(kwargs["title"] or "Video")
    title = title:gsub('"', "&quot;")
    local html = '<div class="quarto-video ratio ratio-16x9"><iframe src="https://www.youtube-nocookie.com/embed/' .. id ..
      '" title="' .. title .. '" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' ..
      'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
    return pandoc.RawBlock("html", html)
  end
}
