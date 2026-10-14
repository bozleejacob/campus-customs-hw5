# Design Notes — the Campus Customs Agent Desk

A ticket-ops dashboard is, honestly, the kind of thing that's very easy to make boring: a table, a status column, a refresh button. We didn't want that. The brief was explicit — make it something a person would actually *want* to sit at — so we built it around one idea: **watching five agents argue about a hoodie order should feel a little bit alive.**

## The corkboard, not a spreadsheet

Tickets don't live in rows. They live as pinned index cards on a corkboard — slightly rotated at random angles like someone actually tacked them up in a hurry, warm cream paper against the dark control-room background, a little red pushpin glowing at the top of each one. The idea is that a ticket is a physical thing someone handed you, not a database row you're paging through. When you select one it straightens up and locks under a blue outline, like you've pulled it off the board to look closer. Resolved tickets fade slightly and get a green "✓ resolved" badge — satisfying in the same way a checked-off to-do list is satisfying.

## A command center, not a form

Everything *around* the corkboard — the header, the agent feed, the summary cards — lives in a dark navy, almost-midnight control-room palette with soft blue glows, because this is supposed to feel like the back office of a shop that's actually running, not an admin panel. A blinking red "live" dot shows up whenever a ticket is actively being worked, the same visual language as a recording light, so you always know at a glance whether the team is mid-conversation or idle.

## Agents as characters, not log lines

This is the part we leaned into hardest. Each agent gets its own emoji avatar and its own color — Boss is a gold 🧑‍💼, Inventory a blue 📦, Accounting a green 💰, Facilities a purple 🏢, Customer Service an orange 💬 — so the live chat feed reads less like a server log and more like a group chat between coworkers who all have a job to do. Every line fades up into place as it arrives, so new agent chatter feels like it's *happening*, not just appearing. When Boss delegates to Inventory, you see the handoff; when Inventory calls a tool, you see exactly which one and what it asked for. The goal was for a human watching the board to be able to follow the plot without reading a changelog.

## A balance that reacts

The checking balance isn't a static number in a corner — it's a small instrument. It's green by default, and the moment an approved payment clears, the whole widget gives a tiny shake, flashes red, and pops up a "− paid out" note before settling back to green with the new, lower number. Money leaving the shop should feel like it actually happened, not like a silent diff.

## Approval stays a deliberate, human click

Because the whole premise of this shop is "agents can prepare a payment but never make one," the Approve Payment flow is intentionally its own modal, not a quiet background action — you read what the team recommended, fill in (or confirm) the amount and reference, type your own name as the approver, and only then does cash move. If the shop can't afford it, you find out immediately, in plain language, without the modal vanishing and leaving you guessing what happened.

## Why it matters

None of this changes what the dashboard *does* — it still lists tickets, runs the team, shows tool calls, and moves money exactly as specified. But a dashboard someone enjoys checking in on gets checked on more often, and a shop with five agents making real decisions about real tickets is exactly the kind of system you want a human paying attention to.
