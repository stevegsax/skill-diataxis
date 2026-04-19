+++
title = "Writing diataxis.toml"
weight = 21
description = "How diataxis.toml works and how to maintain it"
topic = "structure-document"
covers = ["Creating the [project] section", "Defining topics with slugs, titles, and ordering", "Adding quadrant entries with covers, detail, and guidance", "Linking exercises to tutorials"]
detail = "Walk through building a real diataxis.toml from scratch. Show the TOML after each addition."
+++
In this tutorial, we will build a complete `diataxis.toml` for a recipe
application, adding topics and quadrant entries one at a time. After each
addition, we will look at what changed.

## Starting point

We begin with the project metadata:

```toml
[project]
name = "RecipeApp"
description = "Documentation for the RecipeApp cooking platform"
purpose = """Cooking apps accumulate recipes faster than developers can document \
their APIs. RecipeApp's REST interface lets teams manage recipes, search by \
ingredient, and filter by dietary restrictions — but without clear docs, \
integrators resort to reading source code."""
type = "project-docs"
audience = "Developers integrating with the RecipeApp API"
prerequisites = "Familiarity with REST APIs and JSON"
```

The `purpose` field explains why the project exists and what problems it
solves — it drives the introductory page that readers see first. The `type`
field is either `"project-docs"` (documenting a codebase) or `"learning-path"`
(teaching a subject). RecipeApp is a codebase, so we use `"project-docs"`.

## Step 1: Add a topic

Topics group related content across quadrants. Each topic has a slug (used as
the TOML key), a title, and a description:

```toml
[topics.recipe-management]
title = "Recipe Management"
description = "Creating, reading, updating, and deleting recipes"
complexity = "beginner"
order = 1
```

The `order` field controls the display sequence in navigation. The `complexity`
field (`"beginner"`, `"intermediate"`, `"advanced"`) helps set expectations for
the audience.

## Step 2: Add a tutorial entry

Under the topic, add a `tutorials` section. This tells the system where the
tutorial file lives and what it should contain:

```toml
[topics.recipe-management.tutorials]
file = "tutorials/recipe-crud.md"
status = "draft"
covers = [
    "Creating a recipe via the API",
    "Fetching a recipe by ID",
    "Updating a recipe's ingredients",
    "Deleting a recipe",
]
detail = "Step-by-step walkthrough using curl. Show the JSON response after each request."
guidance = "Use a simple pasta recipe as the running example. Start with POST, then GET to confirm it was created."
```

The `covers` field is the scoring contract — each item is a checkable claim.
When the documentation is scored, the tutorial will be evaluated against these
items.

The `guidance` field contains notes for whoever writes or generates the content.
These notes evolve over time as you learn what works.

## Step 3: Add a reference entry

Now add a reference doc for the same topic:

```toml
[topics.recipe-management.reference]
file = "reference/recipe-api.md"
status = "planned"
covers = [
    "POST /recipes — create a recipe",
    "GET /recipes/{id} — fetch a recipe",
    "PUT /recipes/{id} — update a recipe",
    "DELETE /recipes/{id} — delete a recipe",
    "Recipe JSON schema",
]
detail = "One subsection per endpoint. Tabular parameters and response fields."
guidance = "Mirror the API structure. Use consistent formatting for all endpoints: synopsis, parameters table, example request, example response."
```

Notice the `status` is `"planned"` — the file doesn't exist yet. The build
will warn about missing files but won't fail.

## Step 4: Add a second topic

Add another topic for search functionality:

```toml
[topics.search]
title = "Search"
description = "Finding recipes by ingredients, cuisine, and dietary restrictions"
complexity = "intermediate"
prerequisites = ["recipe-management"]
order = 2
```

The `prerequisites` field lists topic slugs that should be understood first. This
helps with ordering in learning paths and tells content generators what
knowledge they can assume.

## Step 5: Add a how-to entry

```toml
[topics.search.howto]
file = "howto/search-by-ingredient.md"
status = "planned"
covers = [
    "Searching for recipes containing a specific ingredient",
    "Combining multiple ingredient filters",
    "Excluding allergens from results",
]
detail = "Concise. Numbered steps. Assume the reader knows the API basics."
guidance = "Title: 'How to Search Recipes by Ingredient'. Link to the recipe API reference for the full query parameter list."
```

## The complete file

After all additions, your `diataxis.toml` looks like this:

```toml
[project]
name = "RecipeApp"
description = "Documentation for the RecipeApp cooking platform"
purpose = """Cooking apps accumulate recipes faster than developers can document \
their APIs. RecipeApp's REST interface lets teams manage recipes, search by \
ingredient, and filter by dietary restrictions — but without clear docs, \
integrators resort to reading source code."""
type = "project-docs"
audience = "Developers integrating with the RecipeApp API"
prerequisites = "Familiarity with REST APIs and JSON"

[topics.recipe-management]
title = "Recipe Management"
description = "Creating, reading, updating, and deleting recipes"
complexity = "beginner"
order = 1

[topics.recipe-management.tutorials]
file = "tutorials/recipe-crud.md"
status = "draft"
covers = [
    "Creating a recipe via the API",
    "Fetching a recipe by ID",
    "Updating a recipe's ingredients",
    "Deleting a recipe",
]
detail = "Step-by-step walkthrough using curl. Show the JSON response after each request."
guidance = "Use a simple pasta recipe as the running example. Start with POST, then GET to confirm it was created."

[topics.recipe-management.reference]
file = "reference/recipe-api.md"
status = "planned"
covers = [
    "POST /recipes — create a recipe",
    "GET /recipes/{id} — fetch a recipe",
    "PUT /recipes/{id} — update a recipe",
    "DELETE /recipes/{id} — delete a recipe",
    "Recipe JSON schema",
]
detail = "One subsection per endpoint. Tabular parameters and response fields."
guidance = "Mirror the API structure. Use consistent formatting for all endpoints: synopsis, parameters table, example request, example response."

[topics.search]
title = "Search"
description = "Finding recipes by ingredients, cuisine, and dietary restrictions"
complexity = "intermediate"
prerequisites = ["recipe-management"]
order = 2

[topics.search.howto]
file = "howto/search-by-ingredient.md"
status = "planned"
covers = [
    "Searching for recipes containing a specific ingredient",
    "Combining multiple ingredient filters",
    "Excluding allergens from results",
]
detail = "Concise. Numbered steps. Assume the reader knows the API basics."
guidance = "Title: 'How to Search Recipes by Ingredient'. Link to the recipe API reference for the full query parameter list."
```

## What you've learned

You have built a `diataxis.toml` that defines:

- Project metadata with purpose, audience, and prerequisites
- Two topics ordered by complexity
- Entries across three quadrants (tutorial, reference, how-to)
- Scoring contracts via `covers` and content guidance via `guidance`

For the full list of fields and their valid values, see the
[diataxis.toml Schema](../reference/diataxis-toml-schema.html). To understand
why the structure document comes before content, see
[Why Structure First](../explanation/why-structure-first.html).
