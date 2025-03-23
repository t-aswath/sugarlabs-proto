# TODO

- [ ] Implement debounce/throttle mechanism for efficiency.
    - [x] throttle
    - [~] debounce
- [x] Improve handling of overlapping trrigers.
- [x] Enhance result formatting for better readability.
- [x] Add auto-complete suggestions.
- [x] Improve accuracy of sentence indexing.
    - **OPTIONS**:
        - **use GREP**
        - ~~improve models reponse by providing more context~~
- [ ] Improve JSON response formatting.
    - [x] Pydantic schema
    - [~] OutputFixingParser
    - [x] Better prompt
- [ ] Logging

# CHORE

- [x] Gtk Cleanup
- [X] Use langchain_ollama instead of ollama-python
- [x] Backend cleanup
    - [x] Remove unused code
    - [x] Remove unused imports
    - [x] Keeping it minimal

# SUGGESTIONS

- [ ] (Walter) Make the `reason` child friendly aka use of simpler words to make it more understandable.
    - **OPTIONS**:
        - Passing the reasons through llm using `abatch`
          ` and `prompt` to simplify the language.
