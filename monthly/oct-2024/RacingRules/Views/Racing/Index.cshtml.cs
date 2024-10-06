using Microsoft.AspNetCore.Mvc.RazorPages;
using RacingRules.Services;

namespace RacingRules.Views.Racing;

public class Index(List<Participant> participants) : PageModel
{
    public List<Participant> Participants { get; } = participants;
}