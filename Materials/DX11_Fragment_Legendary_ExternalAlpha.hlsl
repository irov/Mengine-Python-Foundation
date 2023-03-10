float4 uvsl;

float3 u_color0;
float3 u_color1;
float u_scale0x;
float u_scale0y;
float u_scale1x;
float u_scale1y;
float u_timefactor;
float u_timescale;
float u_timeamplitude;
float u_factor;
float4 u_color;

Texture2D tex0 : register(t0);
Texture2D tex1 : register(t1);
SamplerState sampler0 : register(s0);
SamplerState sampler1 : register(s1);

struct v2p
{
    float4 position : SV_POSITION;
    float4 color : COLOR0;
    float2 uv0 : TEXCOORD0;
    float2 uv1 : TEXCOORD1;
};

struct p2f
{
    float4 color : COLOR0;
};

float sRGB( float t )
{
    return lerp( 1.055 * pow( abs( t ), 1.0 / 2.4 ) - 0.055, 12.92 * t, step( t, 0.0031308 ) );
}

float3 sRGB( in float3 c )
{
    return float3 (sRGB( c.x ), sRGB( c.y ), sRGB( c.z ));
}

void main( in v2p IN, out p2f OUT )
{
    float4 tex0_color = tex0.Sample( sampler0, IN.uv0 );
    float tex1_alpha = tex1.Sample( sampler1, IN.uv1 ).w;

    float ux = (IN.uv0.x + uvsl.x) * uvsl.z;
    float uy = (IN.uv0.y + uvsl.y) * uvsl.w;

    float tx = (ux - 0.5) * cos( u_timefactor * u_timeamplitude ) * u_timescale;
    float ty = (uy - 0.5) * sin( u_timefactor * u_timeamplitude ) * u_timescale;

    float3 col1 = u_color0 + float3(float2(u_scale0x * tx, u_scale0y * ty), 0.0);
    float3 col2 = u_color1 + float3(float2(u_scale1x * ty, u_scale1y * tx), 0.0);

    float3 col = lerp( col2, col1, ux * uy );

    col = sRGB( col );

    OUT.color = IN.color * tex0_color * float4(col, tex1_alpha);
}
