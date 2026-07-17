package com.krishna.ai_client.model;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data

@NoArgsConstructor

@AllArgsConstructor

public class AiRequest {
    private String message;
    private String systemPrompt = "You are a helpful assistant";
    
}
