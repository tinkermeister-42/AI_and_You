local function h2(title, id, classes)
  classes = classes or {}
  return pandoc.Header(
    2,
    pandoc.Inlines(title),
    pandoc.Attr(id or "", classes)
  )
end

-- Lesson section headings.  The order in a lesson is:
--   warmup, learn, tryit, bigq, watch, further
return {
  warmup = function(args, kwargs, meta)
    return h2("🔥 Warm Up", "warmup", {"unnumbered"})
  end,

  learn = function(args, kwargs, meta)
    return h2("👥 Learn Together", "learn", {"unnumbered"})
  end,

  tryit = function(args, kwargs, meta)
    return h2("🛠️ Try It", "try-it", {"unnumbered"})
  end,

  bigq = function(args, kwargs, meta)
    return h2("🧠 The Big Question", "big-question", {"unnumbered"})
  end,

  watch = function(args, kwargs, meta)
    return h2("📺 Watch", "watch", {"unnumbered"})
  end,

  further = function(args, kwargs, meta)
    return h2("🚀 Go Further", "go-further", {"unnumbered"})
  end,

  practice = function(args, kwargs, meta)
    return h2("✍️ Practice On Your Own", "practice", {"unnumbered", "pagebreak-before"})
  end,

  interact = function(args, kwargs, meta)
    return h2("▶️ Interactive Learning", "interactive", {"unnumbered"})
  end
}
