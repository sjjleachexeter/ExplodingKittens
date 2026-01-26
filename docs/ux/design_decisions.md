## Overview
(key design choices, rationale, and trade-offs - a summary)

## Visual Design & Branding

Things like: "We're using green because it reminds people of sustainability"

"We're also using purple because they guy with the money said so"

"We want black outlines because..."

"Times new Roman font, because... idk, we probably won't use that font but it's the kind of thing i'd talk about here"

## Layout & Navigation

### Bottom navigation (mobile):
On mobile, the application uses a persistent bottom navigation for core actions (Home, Missions, Scan, Leaderboard, Profile).
Icons are used instead of text to prevent wrapping on small screens.
Each icon includes an accessible label so functionality remains clear to screen readers.

### Top navigation (desktop):
On larger screens, navigation is displayed at the top to match common desktop conventions.
Core actions use both icons and text, as space constraints are reduced and readability is improved.

### Consistency across devices:
Both layouts use the same routes and page structure, ensuring consistent behaviour across devices.

### Scrolling behaviour:
Core pages (Home, Scan, Missions overview, Leaderboard, Profile) are designed so key actions are visible immediately without scrolling, supporting quick, mobile-first interactions.

Scrolling is used only on pages with more detailed content, such as product passports, mission selection, and informational pages.

This approach prioritises clarity and ease of use for frequent actions, while still supporting more detailed exploration when needed.


## Responsive Design

Most users are expected to access the application on a phone, so the interface uses a mobile-first approach to support scanning and quick interactions on small screens.

On larger screens, layouts adapt to make better use of available space while keeping the same pages and interactions, ensuring a consistent experience across devices. Adjustments to spacing, navigation placement, and typography help avoid the interface feeling sparse or unfinished. A constrained content width is also used to support this


## Accessibility Considerations

Colour contrast etc.

## UX Trade-offs & Constraints

Why X over Y

## Things Deferred or Rejected

For things not done/included and why


## Page-specific considerations
### Home Page
some stuff
### Missions Page
stuff
### Leaderboard Page
stuff
### Profile Page
text
[img]

### Scan Page
|a|b|c|
|-|-|-|
|a|b|c|
|a|b|c|
|a|b|c|
