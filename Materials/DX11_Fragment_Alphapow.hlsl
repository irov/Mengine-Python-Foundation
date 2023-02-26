uniform float u_pow;

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
    float4 color = tex0.Sample( sampler0, IN.tex0 );

    color.w = pow( color.w, u_pow );

    OUT.color = IN.color * color;
}
