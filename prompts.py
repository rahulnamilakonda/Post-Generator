from langchain_core.prompts import PromptTemplate

generationPrompt = PromptTemplate.from_template(
    """Task:
You are a professional social media content strategist. Generate a high-quality post for:
Platform: {platform}
Topic/Context: {topic}

Requirements:
- Add a story as to around the topic, it could be a friend who is confussed or While I'm working this has come, something similar which is catchy.
- Tailor tone & style based on the platform.
- Post length should not be more than 1000 characters based on platform + topic.
- First line should be a strong hook.
- Encourage users to click the link naturally.
- Include a subtle call to action asking for comments or engagement.
- Add 3-6 platform-appropriate hashtags.
- Do NOT hallucinate any details outside the provided topic.
- Do NOT use placeholders like “read more here”.
- Deliver ONLY the final post.
- Please add any documentation links if there exits.
- Create a FOMO to the reader.

Generate the final social media post now:""",
)

notesPrompt = PromptTemplate.from_template(
    """
You are a world-class learning assistant who specializes in extracting
high-quality study notes from educational content.

Task:
Given the YouTube Transcript:
{transcript}

Use ONLY the transcript content (no external assumptions) to generate:
1. **Ultra-concise study notes**
2. **Key ideas + core explanations**
3. **Important definitions / formulas (if any)**
4. **Step-by-step breakdowns of complex concepts**
5. **Real-world examples mentioned in the video**
6. **High-yield revision points for exam or interview prep**
7. **Memory hooks or analogies ONLY if they appear naturally in transcript**
8. **A final “5-Second Revision Summary” with the top 5 must-remember points**

Rules:
- Do NOT hallucinate anything not present in the transcript.
- Do NOT add assumptions or outside knowledge.
- Keep notes crisp, structured, and easy for revision.
- Maintain accuracy above everything.
- If the transcript is missing or incomplete, return a safe message.
- Keep total output within 1500–2000 characters (ideal for revision).
- Deliver ONLY the final notes—no explanations of your process.

Now extract the study notes from the provided video's transcript.
"""
)

evaluationPrompt = PromptTemplate.from_template(
    """
Task:
You are a senior social media strategist and content quality auditor. 
Strictly Evaluate the following post based on its suitability for the specified platform.

Platform: {platform}  (LinkedIn | X-(Twitter) | Instagram)
Generated Post:
"{post}"

Evaluation Requirements:
1. Platform Fit:
   - Is the tone, style, and formatting appropriate for the platform?
   - Does the length match platform expectations?

2. Hook Quality:
   - Is the opening line strong and attention-grabbing?

3. Clarity & Value:
   - Is the message clear, relevant, and valuable based on the topic?
   - Any unnecessary filler or ambiguity?

4. Engagement Strength:
   - Does it encourage users to visit the link naturally?
   - Is the call-to-action (CTA) strong but not spammy?

5. Hashtag Quality:
   - Are hashtags relevant, non-generic, and platform-appropriate?
   - Are they excessive or missing?

6. Authenticity & Accuracy:
   - Does the post avoid hallucination?
   - Does it stick to the given topic?

7. Human Touch and Not AI written.
   - Does this post has human touch?.
   - Is this post is looking like it is written by AI?.

8. Validate the story.
   - I need a solid storng story around the post if you feel its not solid enough   reject immediately and give feedback for improvement - Very IMPORTANT.
   - Does this story around the post sounding real?.
   - Does this story is not looking as fake one?.

8. Final Verdict:
   - Provide a short explanation (2-4 bullet points).
   - Suggest a concise improved version of the post (under the same constraints), without changing facts or hallucinating.

"""
)
