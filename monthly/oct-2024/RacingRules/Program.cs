using Microsoft.Extensions.Caching.Memory;
using RacingRules.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddMvc();
builder.Services.AddSingleton<MemoryCache>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=home}/{action=Index}/{id?}"
);

app.Run();