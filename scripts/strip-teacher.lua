-- strip-teacher.lua: teacher notes live in the lesson source as
--   :::{.teacher title="Class size"} ... :::
-- They never appear on student pages. scripts/make-teacher-guide.py copies
-- them into the unlisted teacher guide (teacher/index.qmd) before each render.
function Div(el)
  if el.classes:includes("teacher") then return {} end
end
