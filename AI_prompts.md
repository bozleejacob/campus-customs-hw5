# AI Prompt Log — Homework 5

Use this file to record the prompts used while completing the assignment.

## Prompt 1

> Just like in previous assignments, we will create an AI prompts.md file to record all of the prompts throughout this assignment.

## Prompt 2

> Create a problem 2 folder titled Problem 2 - Study the campus customs database

## Prompt 3

> in this folder, open data slash campus underscore customs database. I want you to look through every table in its fields. Copy that original file to data slash campus underscore customs underscore new. With our later problems, we'll update that working copy. I want you to start an output slash harness.md file. For each table, we're going to list the fields in one short line on why that table matters for the agents.

## Prompt 4

> Create a problem 3 folder for the next piece. Titled: Problem 3 - Build the MCP server

## Prompt 5

> I want you to write an MCP server in MPC underscore server slash using fast MCP. It will talk to data slash campus underscore customs underscore new database. We do not need to connect or run it in this problem. All the agents we create in this homework will use tools in this MCP server. We're going to add more and more tools later, but for now, let's write three tools we know we'll need for the tickets in the database. Let's keep the names clear. Reminder, never invent any data only use information database in our output slash harness file list each of those three MCP tools for each tool I need to know which table it reads which ticket it helps unlock Parentheses 101 102 103 close parentheses and one sentence on why that tool is the right one for that ticket. Vague lines like reads inventory score low. Make sure we tie the tool to the ticket. Lastly, we want to add a short MCP underscore server slash readme.md file that explains what this MCP server is for which database file it uses and then those three tools that it has

## Prompt 6

> Create problem 4 folder. Titled: Problem 4 - Add the MCP server to vibe coder and test each tool

## Prompt 7

> In our Vibe Coder Claude Code, I want to add our MCP server to the project we're currently working on, which is project or homework five. So our Vibe Coder can call the tools. Then let's save the connection JSON text in .mcp.json. At our project root., Claude Code, I want to add our MP, MCP server to the project we're currently working on, which is project or homework five. So our vibe coder can call the tools. Then let's save the connection JSON text in .mcp.json at our project root. Once we do that, I want to test each of the three MCP tools and save the evidence in a file called output slash MCP underscore smoke dot JSON.

## Prompt 8

> The problem also says I need to test each of the three MCP tools and then save the evidence in output slash MCP underscore smoke dot JSON. Then it says for every tool, include the prompt you ask the vibe coder, the tool name, the tool output, and that tool output must match values in data slash campus underscore customs underscore new database. Do you understand what I'm supposed to do?

## Prompt 9

> Did it restart the session

## Prompt 10

> Ok I restarted it, check again

## Prompt 11

> Try option 1, open a terminal and approve it

## Prompt 12

> check again

## Prompt 13

> Restarted it, check again

## Prompt 14

> check again

## Prompt 15

> closed the whole thing

## Prompt 16

> Create problem 5 folder. titled: Problem 5 - Build the agent team and grow the MCP tools

## Prompt 17

> All right, we're going to build the agentic team for campus customs using pedantic AI, boss, inventory, accounting, facilities, and customer service. Those will be our agents. I want you to include prompts, models, and agent loops so they can delegate work to each other with full connectivity. Let's make sure we put the agent prompts in backend slash prompts slash one file per agent. And we also want to put data types in backend slash models.py. And the agent files under backend slash. Note that for the backend slash, the layout can vary as long as the five roles are clear. Uh, I want to use my port key API key, and we only want to use Luna for every agent. I want to add any tools to the agent or agents need to the MCP server so that we can work on the open tickets. The shop facts should come from the MCP server over data slash campus underscore customs underscore new database. Do not invent a second shop tools. Layer that bypasses the MCP. I want to wire the agents so they append to output slash audit underscore trail.json as they run. And for each agent loop step, record enough to audit later and append to this file. Please do not wipe it each run. In our output slash harness.md file, I want to list each agent and each MCP tool, along with which table the tool uses. Lastly, I want to add a short safety section um, for guardrails a real business would want when agents touch real customers and real money. And I also want some guardrails to make sure that we limit the token usage in each check.

## Prompt 18

> Creat problem 6. Titled Problem 6 - plan the three tickets

## Prompt 19

> Before we wire the backend, I want us to write down what we expect the team to do on each open ticket. Build output slash desk underscore tickets dot html. I want this page to be something we can double click with one tab per ticket, 101, 102, and 103. Also, I want to add empty cache and reflection tabs for later problems. On each ticket tab, I want to fill an expected section and leave room for an actual section that we'll fill out later when we actually run the agents. For each ticket's expected section, I want to put who the boss should call first and why. I want to put all the agent delegations we expect, not something like boss calls everyone. And then I want to also include which MCP tools we expect that run to use. Um, and in these like expected plans, don't don't put just every specialist on there. That's kind of a dumb answer. We want something that is that would make sense. Later, we're going to compare what our prediction is here to the actual. Um, results later, but right now just the expected portion.

## Prompt 20

> Create problem 7 folder. titles: Problem 7: Backend routes

## Prompt 21

> So our React front end dashboard that we're going to do in the next problem is going to need a back end that it can call. So in back end slash main dot py, I want to use fast API and add routes that do the following. First, return the three tickets and whenever each is open or resolved. Second, take a ticket ID and run the agent team on that ticket. Three, return recent agent events, what each agent said and which tool they used so the board can refresh. Four, approve a payment or purchase after a human clicks approve. Agents can only prepare the pay. This route is what actually changes cash. Five, return the current checking balance from cash accounts. Six, reset the database to the original values when you want to try a fresh run.

## Prompt 22

> from the backend/ folder, start the server with: uvicorn main:app --reload --port 8000.
>
> This turns on the backend at http://localhost:8000 so the frontend can call routes. In output/harness.md, list each route in one line (URL/what it does)

## Prompt 23

> Create problem 8 folder, titled Problem 8 - Agent dashboard

## Prompt 24

> I want to build the front-end dashboard in front-end slash. With React plus Vite plus TypeScript. I want this page to call all the routes we built in problem seven. And the board should, one, list all three tickets, two, let you pick one ticket and start the agent team on it, three, show each agent and what they are saying. Well, the ticket runs. Four, mark a ticket resolved when the run finishes. Five, show a short summary of what each agent did on that ticket. Six, let a human approve a pay or purchase when asked. And seven, show the checking balance It should drop if there's an approved pay. I want you to make this dashboard creative and look cool. Um, we want it to be something that a person would want to sit at. So I do want to focus a little bit on making it kind of entertaining.

## Prompt 25

> I want the front end to talk to backend at http://localhost:8000. On the backend, let vite page origin (usually http://localhost:5173) so the browser is allowed to call the routes.
>
> Start the board with npm run dev
>
> Write output/design.md with how we chose the dashboard look and why. Make it sound enjoyable for humans

## Prompt 26

> Create problem 9. Title: Problem 9 - Resolve the tickets

## Prompt 27

> Before we test the agents on a full run, I want to reset the working database, data slash campus underscore customs underscore new database, again, so we can start clean. Note the starting checking balance. Then run all three tickets on the board, tickets 101, 102, 103, until each is resolved. I want you to open output slash desk underscore tickets.html from problem six. On each ticket tab, fill the actual section from this run, which agents worked, what they delegated, and which tools they used. Do not change the expected section. I want to use it to compare. On the cache tab of the same output slash desk underscore tickets.html, I want you to itemize the money, include starting checking balance after the reset, for each ticket, how much cash changed when the ticket was resolved and why, and the ending checking balance, which should match the cash accounts in the working database. Note that wrong cash math is going to make us lose points, even if the board shows every ticket resolved. I want you to save output slash resolved underscore tickets.json for each ticket. It'll include ID, final status, short outcome, what each agent contributed, and any human approvals. And then also save output slash resolved underscore board.html. Which should be a page we can double click with a screenshot of the React board for each resolved ticket, 101, 102, and 103, respectively. Append our real runs to output slash audit underscore trail.json and finish the output slash harness.md file so it covers tables, MCP tools, the five agents, API routes, the dashboard, and safety rules.

## Prompt 28

> Create Problem 10 folder titles Problem 10: Reflection
