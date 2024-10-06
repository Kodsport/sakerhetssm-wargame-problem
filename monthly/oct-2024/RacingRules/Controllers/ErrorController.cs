using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace RacingRules.Controllers;

public class ErrorController : Controller
{
    [IgnoreAntiforgeryToken]
    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Index()
    {
        var exceptionHandler = HttpContext.Features.Get<IExceptionHandlerPathFeature>();
        return exceptionHandler?.Error is NullReferenceException
            ? View(new Views.Error.Index("ssm{race_c0nd1tions_are_fa1lure}"))
            : View(new Views.Error.Index(null));
    }
}