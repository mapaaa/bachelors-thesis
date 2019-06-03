cmake_minimum_required(VERSION 2.8.4)

project(Thesis NONE)

include(UseLATEX.cmake)
add_latex_document(
  thesis.tex
  INPUTS abstract.tex appendix.tex extrapackages.tex introduction.tex layoutsetup.tex macrosetup.tex sections.tex rules.tex theoremsetup.tex typography.tex
  BIBFILES refs.bib)

