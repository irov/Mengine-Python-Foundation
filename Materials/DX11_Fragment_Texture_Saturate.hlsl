float u_factor;

Texture2D tex0 : register(t0);
SamplerState sampler0 : register(s0);

struct v2p
{
    float4 position : SV_POSITION;
    float4 color : COLOR0;
    float2 tex0 : TEXCOORD0;
};

struct p2f
{
    float4 color : COLOR0;
};

void main( in v2p IN, out p2f OUT )
{
    const float3 REC709 = float3(0.2126, 0.7152, 0.0722);
    
    float4 color = tex0.Sample( sampler0, IN.tex0 );

    float l = dot(color.rgb, REC709);
    float3 grayscale = float3(l, l, l);

    float3 saturated = lerp(grayscale, color.rgb, u_factor);

    OUT.color = IN.color * float4(saturated, color.a);
}
