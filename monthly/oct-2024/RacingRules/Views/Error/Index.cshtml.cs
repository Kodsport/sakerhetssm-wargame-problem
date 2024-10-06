using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace RacingRules.Views.Error;

public class Index : PageModel
{
    public Index(string? flag)
    {
        Flag = flag;
    }

    public string? Flag { get; }   
}