# Week 1 Teaching Readiness Design

## Goal

Prepare Week 1 for a two-hour live session from 3:00 PM to 5:00 PM without removing content from the slide deck, student lab, reading, or quiz. The primary implementation focus is making the student notebook understandable without constant instructor interpretation.

## Live Session Design

Use one coherent teaching path:

| Time | Segment | Role |
|---|---|---|
| 3:00-3:10 | Orientation | Set expectations and connect prior Azure experience to Databricks |
| 3:10-3:52 | Slides | Present all 19 slides with teach/skim/reference pacing cues |
| 3:52-4:20 | Notebook Part 2 | Run the only instructor-led demonstration |
| 4:20-4:47 | Notebook Part 3 | Launch the only student hands-on lab; complete one task together |
| 4:47-5:00 | Quiz and close | Ask five selected questions, recap, and assign remaining material for review |

The separate decision-card activity remains an optional verbal checkpoint. It is not a required fourth activity.

## Student Notebook

Keep the existing runnable code, task sequence, and TODO cells. Add learner-facing Markdown before each meaningful code cell with:

- the immediate goal;
- why the step matters;
- what the code is doing;
- what learners should observe after running it;
- relevant exam or engineering context;
- concise hints and success criteria for lab tasks.

Add an early explanation of why Week 1 uses SQL:

- SQL is concise and declarative for table, metadata, governance, and query operations;
- SQL is directly relevant to the certification objectives;
- PySpark/Python is appropriate for programmatic transformations, control flow, reusable logic, and orchestration;
- Scala uses the Spark JVM API and is useful in some engineering codebases, but it is not the primary language for this Week 1 learning goal;
- Databricks notebooks can mix languages, as demonstrated by Python setup code calling Spark SQL and `%sql` cells for database work.

Use a hybrid live-delivery pattern: type the first high-value examples, then paste or run later prepared cells when syntax becomes repetitive.

Replace the learner-visible private solution-path text with: "The solution file will be shared by your instructor."

## Instructor Notes

Reorganize the live-delivery portion to match the student notebook exactly. Place explanation before the related code so the instructor does not need to scroll backward.

For every demo step, use this order:

1. Goal
2. What to say
3. Type or paste guidance
4. Prediction question before running
5. Expected result
6. Recovery or skip guidance

Retain deeper reference material where useful, but separate it from the live runbook so it does not interrupt delivery. Explicitly distinguish:

- instructor demo: Notebook Part 2;
- student hands-on lab: Notebook Part 3;
- optional in-class checkpoint: verbal decision cards;
- assessment: five live quiz questions, with the full quiz available for review.

## Student Reading

Validate `readings/Week1_Lakehouse_Foundations.md` as a student handout. Check technical accuracy, consistency with the notebook and slides, independent readability, language-choice explanation, and clear after-class expectations. Make targeted edits only where they improve correctness or learner understanding.

## Slides And Quiz

Preserve the PowerPoint and all quiz questions. Audit them for technical correctness, alignment, timing, and delivery risk. Modify only factual or blocking issues.

Mark five quiz questions for live use in the instructor notes. The full 13-question quiz remains available for independent review.

## Repository-Wide Solution Message Cleanup

Replace learner-visible messages that expose `instructor_private` paths or git-ignore details in the Week 1, 2, 4, and 5 notebooks. Use neutral wording stating that the solution file will be shared by the instructor.

Do not remove legitimate instructor-only repository documentation from private notes or the README.

## Validation

- Parse the Databricks source notebooks and verify cell boundaries remain valid.
- Check that every executable Week 1 notebook cell has useful preceding learner context.
- Verify TODO tasks, hints, expected outputs, and validation criteria agree with the solution.
- Audit the reading and quiz against the Week 1 objectives.
- Verify the PowerPoint renders without visible defects and that its claims align with the other artifacts.
- Search learner-facing files to confirm private solution paths and git-ignore language are gone.
- Produce a concise teaching-readiness verdict with remaining risks, if any.
