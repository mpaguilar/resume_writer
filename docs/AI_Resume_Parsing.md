---
kind: essay
date: "2024-08-04"
time: "17:21"
tags: recruiting, resume, AI, LLM
---

# Resumes and Automatic Tracking Systems

Has a job site asked you to upload your resume, then tried to parse it? Did it work? In many cases, no, it didn't.

A lot of job sites ask candidates to upload their resume as a MS Word .docx file, and attempt to parse the fields. The fields are then put into a recruiting-specific application known as an Automatic Tracking System (ATS). Recruiters, and sometimes hiring managers, can then query the ATS looking for specific skills and other candidate qualities to help them narrow down whom to contact.

The parsing often fails, often to the point of uselessness. Compounding the issue is that a human-friendly resume, attractive to hiring managers, often contains formatting elements that make parsing difficult. Elements like tables, bullet-points, etc., make it more difficult.

The underlying problem is how MS Word, as well as PDF, HTML, and other formats, represent the data.

# What you see is what you get, but that's not how it's stored

MS Word is designed so the user will have an accurate on-screen representation of what will be printed. It's pretty good at this, as many professionals will attest. Maybe not perfect, but pretty good.

Underneath the visual representation is where things get complicated. There are few, if any, correlations between the data as shown on screen and how it is stored in the file. 

For example, a table may have two columns, each with a different number of rows. Just because the rows line up in the editor doesn't mean they are next to each other in the data. It may be stored with all of the data in the left column first, followed by all of the data in the second column. They are "connected" internally for visual representation via other codes saying, essentially, "put this text into a column here, and this text into a column over there."

There's no way to tell that the rows are related to one another without rendering the document visually.

Heavy users of Word report plenty of horror stories of a document looking great in one version of Word, and looking completely messed up in a different version of Word. A document created in Online MS Word may not look the same in the desktop version, even if both are completely updated. That same document opened in LibreOffice (an open source editor) may render completely differently.

Making even more difficult is that a clean-looking document may be a mess as data. If you ever "show formatting marks" in typical Word document, you're likely to see a mess of glyphs that have no effect on the output, at least until something strange is displayed.

# Word documents are pictures

A Word document isn't that much different than a picture. There is no information in them that says "this section refers to skills acquired at that job". It isn't until is visually rendered that the association is clear.

Unlike pictures, Word documents can produce the same output with completely different input. How it is represented as data can be dependent on the order in which it was added. A jpeg has a single way to store the data for a picture, where a Word document may have a half-dozen ways to store the data.

# Why not AI?

This disconnect between visual representation and data storage leads to significant parsing issues, giving AI significant challenges to parsing resumes, but it is possible. Currently, there is a lot of activity and stumbling around in this space, and so far the results have been underwhelming. 

The problem lies in training. This is a topic that comes up every time the idea of "use AI to solve it" comes up. Machine learning isn't magic. Simply throwing unstructured data into a neural net results in garbage.It took several years of iterations, extensive training, and immense processing power before text LLMs (like ChatGPT) became sufficiently advanced to be useful. Text is relatively well-structured.

To get good results from an AI, it needs data that is labeled correctly. There is nothing in a picture that says "that's a stoplight". It's only by visually inspecting the picture that a stoplight can be identified. Humans are good at this, a raw neural net isn't. Humans have been used to label millions of pictures so an AI can "learn" what pictures have a stoplight, and which ones don't.

# What it takes to train AI on resumes

Resumes would have to follow the same process as any other picture. Humans would have to look at a rendered resume and label the different parts. After running the labeled data through a neural net, the output has to be verified against the original data. There are tools to help with this, but in the end it is a manual process. It takes time, and ends up being expensive in labor costs. 

That doesn't mean it won't be done. There are people out there much smarter than me working on the problem right now. I don't think any solution will be ready this year, or even next. I'm sure we'll see some improvements, but the underlying problems remain the same. 

The data is unstructured, and unlabeled. The same output can be represented in the data in many different ways. The data may contain garbage which is invisible when rendered.

A tough problem, but not unsolvable. Someone will do it, just not soon.