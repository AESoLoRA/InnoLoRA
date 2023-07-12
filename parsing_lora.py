# -*- coding: utf-8 -*-
"""LoRA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lcf2bg45sdzZS9pTZxfgygmU7UiQU0en
"""

import PyPDF2
import json

def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()

    return text

# Example usage
pdf_path = "/content/XXXX.pdf"
output_text = pdf_to_text(pdf_path)

data = {
    "extracted_text": output_text
}

json_data = json.dumps(data)
parsed_json = json.loads(json_data)

extracted_text = parsed_json["extracted_text"]
pages = extracted_text.split("\f")
for i, page in enumerate(pages):
    print(page)

!pip install PyPDF2
!pip install transformers

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Load the T5 model and tokenizer
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


# Example text
text = """
when p m = if p then m else return ()
main = do args <- getArgs
          when (null args)
               (putStrLn "No args specified!")
If you notice a repeated expression pattern, like

if c then t else False
you can give this a name, like

and c t = if c then t else False
and then use it with the same effect as the original expression.

Get code re-use by composing lazy functions. It's quite natural to express the any function by reusing the map and or functions:

any :: (a -> Bool) -> [a] -> Bool
any p = or . map p
Reuse the recursion patterns in map, filter, foldr, etc.
"""
# Preprocess the input
inputs = tokenizer.encode("generate questions: " + text, return_tensors="pt")

# Generate questions
outputs = model.generate(inputs, max_length=64, num_return_sequences=5, do_sample=True)

# Decode and print the generated questions
for i, output in enumerate(outputs, 1):
    generated_question = tokenizer.decode(output, skip_special_tokens=True)
    print(f"Question {i}: {generated_question}")

!pip install sentencepiece

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Load the T5 model and tokenizer
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Example text about Haskell
text = """
Haskell is a functional programming language that emphasizes purity, laziness, and strong static typing. It is widely used in the field of academia and has gained popularity in industry applications as well. Haskell's type system allows for robust and concise code, and its focus on immutability and referential transparency promotes code reliability and easier testing.

Some key features of Haskell include type inference, pattern matching, higher-order functions, and list comprehensions. It also provides support for monads, which facilitate handling side effects in a pure functional setting.

Haskell has a rich ecosystem of libraries and tools, making it suitable for a wide range of applications. It is often used in areas such as financial modeling, compiler development, and formal verification.

Learning Haskell can be challenging for beginners due to its unique syntax and the functional programming paradigm. However, it offers a powerful and elegant way to solve complex problems and encourages writing code that is concise, modular, and maintainable.
"""

# Preprocess the input
inputs = tokenizer.encode("generate questions: " + text, return_tensors="pt")

# Generate questions
outputs = model.generate(inputs, max_length=64, num_return_sequences=5, do_sample=True)

# Decode and print the generated questions
for i, output in enumerate(outputs, 1):
    generated_question = tokenizer.decode(output, skip_special_tokens=True)
    print(f"Question {i}: {generated_question}")

from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Load the T5 model and tokenizer
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Example text about Haskell
text = """
Haskell is a functional programming language that emphasizes purity, laziness, and strong static typing. It is widely used in the field of academia and has gained popularity in industry applications as well. Haskell's type system allows for robust and concise code, and its focus on immutability and referential transparency promotes code reliability and easier testing.

Some key features of Haskell include type inference, pattern matching, higher-order functions, and list comprehensions. It also provides support for monads, which facilitate handling side effects in a pure functional setting.

Haskell has a rich ecosystem of libraries and tools, making it suitable for a wide range of applications. It is often used in areas such as financial modeling, compiler development, and formal verification.

Learning Haskell can be challenging for beginners due to its unique syntax and the functional programming paradigm. However, it offers a powerful and elegant way to solve complex problems and encourages writing code that is concise, modular, and maintainable.
"""

# Preprocess the input
inputs = tokenizer.encode("generate questions: " + text, return_tensors="pt")

# Generate questions
outputs = model.generate(inputs, max_length=64, num_return_sequences=5, do_sample=True)

# Decode and print the generated questions
for i, output in enumerate(outputs, 1):
    generated_question = tokenizer.decode(output, skip_special_tokens=True)
    print(f"Question {i}: {generated_question}")

from transformers import pipeline

# Load the question-answering pipeline
question_answering_pipeline = pipeline("question-answering")

# Example context
context = """
Haskell is a functional programming language that emphasizes purity, laziness, and strong static typing. It is widely used in the field of academia and has gained popularity in industry applications as well. Haskell's type system allows for robust and concise code, and its focus on immutability and referential transparency promotes code reliability and easier testing.

Some key features of Haskell include type inference, pattern matching, higher-order functions, and list comprehensions. It also provides support for monads, which facilitate handling side effects in a pure functional setting.

Haskell has a rich ecosystem of libraries and tools, making it suitable for a wide range of applications. It is often used in areas such as financial modeling, compiler development, and formal verification.

Learning Haskell can be challenging for beginners due to its unique syntax and the functional programming paradigm. However, it offers a powerful and elegant way to solve complex problems and encourages writing code that is concise, modular, and maintainable.
"""

# Example question
question = "What are the ideas"

# Perform question answering
result = question_answering_pipeline(question=question, context=context)

# Print the answer
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['score']}")

