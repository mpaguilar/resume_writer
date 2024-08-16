# Resume Writer

This is a simple resume writer that takes a text file and converts into a Word document. The current output is very plain, making it more likely to be successfully parsed by Automatic Tracking Systems (ATS).

This helps applicants to quickly adapt resumes to different job applications. When copying from LLM output, authors don't have to worry about messing up the doc formatting.

For recruiters receving generated applications, it's easier for them to add and update resumes to their ATS.

## Sample output

The output is very plain. If you're looking for an impressive resume with lots of tables, this isn't it. Things like tables, bullet points, icons, and colors are difficult for ATS to parse.

## Sample input

The test file is the best way to see how the input should be formatted. It's in the source code [here](https://raw.githubusercontent.com/mpaguilar/resume_writer/main/tests/test_resume.md)


## Creating a new resume

The input file is _data_, not a document. Even though it is text, it is structured. Heading indentation must be respected, and the heading names must be correct. No formatting should be added, any text will be added to the document as-is. For example, adding `*bold*` to the text will add "*bold*" to the document. The text will not be bolded. This is true of tables, extra tabs, etc.

[!NOTE]
Date format is very picky, and must be in the format `MM/YYYY`. Improving date parsing is a very high priority. 

## How to create a new style of document

`resume_render/basic` has a full test suite. To create a new style of resume:
- copy the `basic` folder
- rename the file prefix from `basic_` to `<your_style>_`
- update the imports in `resume_render/<your_style>/<your_style>_resume.py`
- hack away

## Making changes to `resume_render/basic`
The basic renderer has a full test suite. If any logic changes are required, update the tests.


## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the LICENSE file for details.
