# Q&A Agent DSPy Optimization Project

## Requirements Summary

### Problem Statement
The current Q&A requirements clarification agent uses a hand-crafted prompt that may not optimally elicit the critical missing information from user problem statements. The goal is to use DSPy with MIPRO optimization to refine the question-asking portion of the prompt, training it to identify and ask about information gaps that significantly impact the final implementation.

### Requirements

#### Functional Requirements
- Create synthetic training data: problem statements with intentionally omitted critical details
- Define expected questions for each problem statement (what should be asked)
- Implement LLM-as-judge metric to semantically match generated questions to expected questions
- Use DSPy/MIPRO to optimize the question-generation prompt
- Preserve structural behaviors (conflict detection, periodic synthesis) as hard-coded or separate modules
- Support iterative refinement of training data based on discovered good questions

#### Non-Functional Requirements
- Train on smaller/cheaper model, deploy optimized prompt on larger model (Opus)
- Judge model should be small but capable of reasoning (e.g., GPT-4o-mini or similar)
- High-quality training examples preferred over quantity (20-30 examples target)
- Optimization should improve question coverage without excessive irrelevant questions

### Constraints & Boundaries
- Only optimizing the question-asking portion, not synthesis or conflict detection
- Structural behaviors (numbered questions, periodic synthesis) stay in prompt wrapper
- Must handle the "good questions we didn't anticipate" problem gracefully
- Training data requires manual curation and iterative refinement

### Technical Context
- Framework: DSPy with MIPRO optimizer
- Current prompt: `agent/primary/qa.md` (222 lines)
- Target deployment model: Claude Opus (or similar high-capability model)
- Training model: Smaller model (Sonnet, Haiku, or similar)
- Judge model: Small reasoning model (GPT-4o-mini, Claude Haiku, etc.)

### Decisions Made
- Structural behaviors hard-coded in wrapper OR composed as separate modules (TBD based on metric feasibility)
- LLM-as-judge uses different (smaller) model than the one being optimized
- Start with 20-30 high-quality synthetic examples
- Iteratively refine training data by reviewing generated questions and adding good unexpected ones
- Success metric: Ask most expected questions, minimize but tolerate some extra questions

### Out of Scope
- Optimizing the synthesis/summary generation portion
- Optimizing conflict detection behavior
- Fine-tuning models (using prompt optimization only)
- Production deployment automation

---

## Detailed Project Understanding

### The Core Problem

The Q&A agent's job is to extract requirements from vague or incomplete user descriptions. The current prompt provides guidelines and examples, but:

1. **May miss important questions**: Hand-crafted prompts can have blind spots
2. **No systematic optimization**: Current prompt is based on intuition, not data
3. **Hard to measure quality**: No clear metric for "good questioning"

### What We're Optimizing

The Q&A prompt has several components:

```
+---------------------------+
|   Structural Behaviors    |  <- Hard-coded / separate modules
|   - Conflict detection    |
|   - Periodic synthesis    |
|   - Numbered questions    |
+---------------------------+
            |
            v
+---------------------------+
|   Question Generation     |  <- THIS IS WHAT WE OPTIMIZE
|   - Identify gaps         |
|   - Prioritize questions  |
|   - Ask about boundaries  |
+---------------------------+
            |
            v
+---------------------------+
|   Final Summary Format    |  <- Hard-coded template
+---------------------------+
```

### Training Data Design

Each training example consists of:

1. **Problem Statement**: A realistic user request with intentionally missing critical information
2. **Expected Questions**: The questions that SHOULD be asked to fill the gaps

**Example:**
```
Problem Statement:
"I want to build a website for my restaurant that shows our menu and lets people make reservations."

Missing Critical Information:
- Styling approach (CSS framework? Design system?)
- Tech stack (static site? React? WordPress?)
- Reservation system (build custom? Integrate with existing?)
- Payment processing needed?
- Mobile responsiveness requirements?
- Hosting preferences?

Expected Questions:
1. "What technology stack are you considering - a static site, a framework like React/Next.js, or a CMS like WordPress?"
2. "For styling, do you have a preference for CSS approach - Tailwind, a component library like shadcn, or custom CSS?"
3. "Should the reservation system be built custom, or integrate with an existing service like OpenTable or Resy?"
4. "Will customers need to pay a deposit when making reservations, or is payment handled separately?"
5. "Are there specific mobile requirements, or is standard responsive design sufficient?"
...
```

### The Metric Challenge

The LLM-as-judge needs to:

1. **Match questions semantically**: "What CSS framework?" and "How do you want to handle styling?" are asking the same thing
2. **Score coverage**: What percentage of expected questions were asked (in some form)?
3. **Penalize irrelevance**: Dock points for questions that don't matter, but carefully
4. **Handle surprises**: Don't penalize genuinely good questions that weren't in the expected set

**Proposed Metric Structure:**
```python
def evaluate_questions(generated_questions, expected_questions, problem_statement):
    # Use LLM judge to:
    # 1. Match each generated question to expected questions (semantic similarity)
    # 2. Calculate coverage: matched_expected / total_expected
    # 3. Calculate precision: matched_generated / total_generated
    # 4. Flag potentially good unmatched questions for human review
    
    # Return weighted score favoring coverage over precision
    return coverage * 0.7 + precision * 0.3
```

### The "Good Unexpected Questions" Problem

This requires an iterative approach:

1. **Initial training set**: Create 20-30 examples with expected questions
2. **Run optimization**: Train the model
3. **Review outputs**: Look at questions the model asked that weren't expected
4. **Curate**: Add genuinely good questions to the expected set
5. **Repeat**: Re-run optimization with enriched training data
6. **Converge**: Stop when the model stops surfacing new good questions

### Module Composition Approach

If structural behaviors become separate DSPy modules:

```python
class QAAgent(dspy.Module):
    def __init__(self):
        self.question_generator = OptimizedQuestionGenerator()  # <- Optimized
        self.conflict_detector = ConflictDetector()  # <- Fixed prompt
        self.synthesizer = Synthesizer()  # <- Fixed prompt
    
    def forward(self, problem_statement, conversation_history):
        # Check for conflicts first
        conflicts = self.conflict_detector(conversation_history)
        if conflicts:
            return self.handle_conflicts(conflicts)
        
        # Generate questions (the optimized part)
        questions = self.question_generator(problem_statement, conversation_history)
        
        # Periodic synthesis
        if should_synthesize(conversation_history):
            synthesis = self.synthesizer(conversation_history)
            return synthesis + questions
        
        return questions
```

This allows optimizing question generation independently while keeping other behaviors stable.

### Transfer Learning Assumption

Training on a smaller model (e.g., Sonnet) and deploying on a larger model (Opus):

- **Why it works**: Prompts that work well on constrained models often work even better on capable models
- **Caveat**: May not be optimal for Opus specifically, but should be "good enough"
- **Alternative**: Could do final tuning on Opus with fewer iterations if needed

### Success Criteria

Qualitative:
- The optimized prompt asks most of the "obvious" questions humans would ask
- Doesn't waste time on irrelevant tangents
- Surfaces non-obvious but important questions

Quantitative (rough targets):
- Coverage: 80%+ of expected questions asked
- Precision: 70%+ of asked questions are relevant
- Iterate until satisfied with real-world usage

### Implementation Phases

**Phase 1: Training Data Creation**
- Create 20-30 diverse problem statements across domains (features, bugs, architecture, etc.)
- Define expected questions for each
- Ensure variety in what's "missing" (tech choices, scope, constraints, etc.)

**Phase 2: Metric Implementation**
- Implement LLM-as-judge for semantic question matching
- Test metric on hand-crafted examples to validate it works
- Tune matching threshold and scoring weights

**Phase 3: DSPy Setup**
- Create DSPy signature for question generation
- Wrap structural behaviors in fixed prompt sections
- Set up MIPRO optimizer with the metric

**Phase 4: Optimization Loop**
- Run initial optimization
- Review generated questions for good unexpected ones
- Update training data
- Repeat until convergence

**Phase 5: Deployment**
- Extract optimized prompt
- Integrate into qa.md (or create new optimized version)
- Test on real problem statements
- Iterate if needed

### Open Questions for Future Exploration

1. Should we optimize for different domains separately (features vs bugs vs architecture)?
2. How do we handle the cold-start problem (no conversation history yet)?
3. Should the number of questions be part of the optimization, or fixed?
4. Could we use the optimized prompt to help generate more training data?
