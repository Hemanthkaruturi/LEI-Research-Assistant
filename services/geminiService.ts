
import { GoogleGenAI } from "@google/genai";
import type { GeminiVerificationResult, GroundingChunk } from '../types';

export const getLegalNameAndSources = async (website: string): Promise<GeminiVerificationResult> => {
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
        
        return { legalName, sources };

    } catch (error) {
        console.error("Error calling Gemini API:", error);
        throw new Error("Failed to verify company name using Gemini API.");
    }
};
