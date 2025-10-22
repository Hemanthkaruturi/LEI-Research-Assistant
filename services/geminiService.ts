
import { GoogleGenAI } from "@google/genai";
import type { GeminiVerificationResultWithCost, GroundingChunk } from '../types';

// Estimated pricing for demonstration purposes.
// Real pricing is based on tokens, but we use characters for this example.
// Based on a model like Gemini 1.5 Flash at ~$0.35/1M input chars & ~$1.05/1M output chars.
const COST_PER_INPUT_CHAR = 0.35 / 1_000_000;
const COST_PER_OUTPUT_CHAR = 1.05 / 1_000_000;

export const getLegalNameAndSources = async (website: string): Promise<GeminiVerificationResultWithCost> => {
    if (!process.env.API_KEY) {
        throw new Error("API_KEY environment variable not set");
    }

    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

    const prompt = `What is the official legal name for the company that owns and operates the website ${website}? Respond with only the legal name and nothing else.`;

    try {
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: prompt,
            config: {
                tools: [{ googleSearch: {} }],
            },
        });

        const legalName = response.text.trim();
        if (!legalName) {
            throw new Error("Gemini API did not return a legal name.");
        }
        
        const sources = response.candidates?.[0]?.groundingMetadata?.groundingChunks as GroundingChunk[] || [];

        // Calculate estimated cost
        const inputChars = prompt.length;
        const outputChars = legalName.length;
        const cost = (inputChars * COST_PER_INPUT_CHAR) + (outputChars * COST_PER_OUTPUT_CHAR);
        
        return { legalName, sources, cost };

    } catch (error) {
        console.error("Error calling Gemini API:", error);
        throw new Error("Failed to verify company name using Gemini API.");
    }
};