# Project Overview

This project is a Quarto-based website for a linear algebra course titled "Álgebra Lineal 2025-2". The website is available at [https://abelalv.github.io/lineal_2025_2/](https://abelalv.github.io/lineal_2025_2/).

The content is in Spanish and is structured into sections (`section*.qmd`) and workshops (`taller*.qmd`).

*   **Sections** cover the theoretical concepts of linear algebra, including vector operations, matrices, determinants, and transformations. They often include Python code examples using `numpy` and `matplotlib` to illustrate the concepts.
*   **Workshops** provide exercises to practice the concepts explained in the sections.

The entire project is configured using the `_quarto.yml` file, which defines the website's structure, navigation, and theme.

## Building and Running

This is a Quarto project. To render the website, you need to have Quarto installed.

The main command to render the project is:

```bash
quarto render
```

This will render all the `.qmd` files and generate the website in the `docs/` directory.

To render a specific file, you can use:

```bash
quarto render <file>.qmd
```

## Key Files

*   `_quarto.yml`: The main configuration file for the Quarto project. It defines the website's structure and sidebar navigation.
*   `index.qmd`: The main page of the website, which contains the course schedule.
*   `section*.qmd`: These files contain the course's theoretical content.
*   `taller*.qmd`: These files contain the workshops and exercises.
*   `styles.css`: Custom CSS for the website.
*   `docs/`: The output directory for the rendered HTML files.

## Development Conventions

The project uses `pyodide` to run Python code in the browser. The Python code blocks are used to illustrate linear algebra concepts and generate plots. The main libraries used are `numpy` for numerical operations and `matplotlib` for plotting.
