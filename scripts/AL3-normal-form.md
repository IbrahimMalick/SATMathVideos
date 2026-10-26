---
scene: shorts.normal_form
---

<!-- Body is the transcript verbatim so the aligner matches exactly. Beats placed by anchor phrase, not by hand-counted word index. -->

[[beat:hook]] Guys, you should be able to solve this if you're an A star computer
science student, okay? [[beat:table]] An enrollment table contains a student ID,
student name, [[beat:fields]] course ID, course name, tutor ID, tutor name, and room.
[[beat:key]] Its composite primary key is a student ID plus course ID. [[beat:fd1]] So
a student ID determines the student name, [[beat:fd2]] course ID determines course
name, teacher ID, and room. Okay. [[beat:fd3]] Tutor ID determines student name.
[[beat:question]] Your challenge is to convert this relation into third normal form.
[[beat:pause]] Pause the video and create the table first. All right. [[beat:solve]]
All right, let's solve it. [[beat:partial1]] A student name depends on a student ID,
not on the complete primary key. [[beat:partial_rule]] That is a partial dependency.
Okay. [[beat:student_table]] So create a student table containing a student ID and a
student name. [[beat:course_fd]] Course name, tutor ID and room depend only on course
ID. [[beat:course_table]] So create a course table containing course ID, course name,
tutor ID and room. All right. [[beat:enrol_table]] And the relationship between the
students and the courses become an enrollment table containing a student ID and course
ID. [[beat:not_finished]] We We're not finished. [[beat:transitive]] The tutor name
depends on tutor ID and tutor ID depends on course ID. [[beat:transitive_rule]] So
that is a transitive dependency. It's called transitive dependency.
[[beat:tutor_table]] So create a tutor table containing tutor ID and tutor name.
[[beat:four_tables]] The final database contains four tables. [[beat:names]] A
student, course, tutor, and enrollment. [[beat:trap]] If you remove only the partial
dependency, you reach second normal form, not third normal form. [[beat:close]] So did
you identify the, did you identify the transitive dependency? If yes, great. If not,
keep trying.
