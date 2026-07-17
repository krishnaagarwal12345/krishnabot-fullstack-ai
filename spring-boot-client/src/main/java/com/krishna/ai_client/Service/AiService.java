package com.krishna.ai_client.Service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import com.krishna.ai_client.model.AiRequest;
import com.krishna.ai_client.model.AiResponse;
import com.krishna.ai_client.model.RagRequest;
import com.krishna.ai_client.model.RagResponse; 
@Service
public class AiService {

     private final WebClient webClient;

    // Inject Python API URL from application.properties
    public AiService(@Value("${ai.api.url}") String aiApiUrl) {
        this.webClient = WebClient.builder()
                .baseUrl(aiApiUrl)
                .build();
    }

    // Call Python /api/chat endpoint
    public AiResponse chat(String message) {
        AiRequest request = new AiRequest();
        request.setMessage(message);

        return webClient.post()
                .uri("/api/chat")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AiResponse.class)
                .block();
    }

    // Call Python /api/chat with custom system prompt
    public AiResponse chatWithPrompt(
            String message, String systemPrompt) {

        AiRequest request = new AiRequest(message, systemPrompt);

        return webClient.post()
                .uri("/api/chat")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AiResponse.class)
                .block();
    }

    // Call Python /api/rag endpoint
    public RagResponse ragQuery(String question) {
        RagRequest request = new RagRequest(question);

        return webClient.post()
                .uri("/api/rag")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(RagResponse.class)
                .block();
    }

    // Check if Python API is healthy
    // Check if Python API is healthy
    public String healthCheck() {
        return webClient.get()
                .uri("/health")
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }
    // Should be like this ✅



    
}
