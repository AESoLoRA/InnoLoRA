# InnoLoRA

## 1. Repository rules ## 

If you want to make an update to the project, please, create a new branch and send it for a pull request. Example: 

  1. Switch to a new branch: `git checkout -b 'branch_name'`
  2. Do the code change
  3. Append the change: `git add .`
  4. Commit: `git commit -m "name of my commit"`
  5. Push to the repo and wait for a review: `git push --set-upstream origin 'branch_name'`

## 2. Useful sources ## 

### 2.1. Data sets and models ###

[The Stack](https://huggingface.co/bigcode)  - open-source code base and the [related](https://arxiv.org/pdf/2107.03374.pdf) paper

[LibGen](https://libgen.is/book/index.php?md5=9D6E704F93465F95A80960EDC42817E3) - textbooks source

[RedPajama](https://www.together.xyz/blog/redpajama-7b) - open-source language model

### 2.2. Training pipeline ###

[Causal language modeling](https://huggingface.co/docs/transformers/tasks/language_modeling) - popular way of language models training by prediction the next word in a sentence

[Textbooks Are All You Need](https://arxiv.org/pdf/2306.11644.pdf) - generation of textbook quality data that allowed to train a relatively small yet efficient model

[LoRA](https://github.com/microsoft/LoRA) - fune-tuning method by matrix decomposition 



### 2.3. Code generation models ###

[Polycoder](https://github.com/VHellendoorn/Code-LMs) - code generation pretrained model + dataset collection scripts

[Codex](https://platform.openai.com/docs/guides/code) - Web inteface only
