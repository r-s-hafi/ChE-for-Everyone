# Pumps

## I got asked this and completely blanked

In a technical interview I had out of college, a senior principal engineer was walking me through a project on my resume and then kind of organically turned it into a troubleshooting question. We ended up on pump curves, and he asked me where the deadhead point was.

I had no idea. I told him I didn't know.

To say the least, it was pretty embarrassing. And what stuck with me is that literally everyone on that plant would call that a basic question, and after a 4.0 GPA through four years of chemical engineering, it had never been brought to my attention.

## What school gave me vs. what I actually needed

My fluids class was almost entirely theoretical. Pulling friction loss coefficients off charts and correlations, and five lectures deriving Navier-Stokes. We had one lecture on pump curves. One.

I have never derived Navier-Stokes at work. I deal with pumps every single day, because you can't have a plant without them (nothing moves anywhere unless something is pressurizing it). So the pump curve isn't some footnote at the end of the chapter, it's a real thing that you need to know to be an effective process engineer.

If you're cramming for a technical interview and only have time for one fluids topic, make it this one.

## What a pump actually does

A pump pressurizes liquid. That's the entire mental model. If you can't pressurize it, you can't move it.

There are two main types you need to know:

**Centrifugal.** A spinning impeller throws liquid outward and that velocity turns into pressure. Most pumps you’ll run into will be centrifugal.

**Positive displacement (PD).** A fixed volume of liquid gets trapped and physically pushed forward every cycle. Gear pumps, screw pumps, diaphragm pumps, reciprocating pumps.

The type of pump dictates everything about how you approach them.

## The stuff that actually matters

### The pump curve

A centrifugal pump curve is a graph of differential pressure (often called differential head) vs. flow, and head drops as flow goes up. There are three key spots on the curve:

**Shutoff head (or deadhead)** is the far left of the curve, at zero flow. This is where your pump would run with the discharge fully blocked in. That's the most pressure a centrifugal pump can physically make.

**Runout** is on the far right. This is where the pump is at max flow and minimum head.

**BEP (best efficiency point)** is somewhere in the middle where the pump functions best.

When something goes wrong with a pump, "where are we on the curve" is basically always the first question.

### "Running off its curve" means the pump is unhappy

If a pump isn't performing where the curve says it should for the conditions you're at, that means the pump has degraded somehow. Worn impeller, worn wear rings, damaged internals. The curve is the manufacturer telling you what a healthy pump does, so falling short of it is evidence something isn't healthy anymore.

### Throttling the discharge

If you close the discharge valve partway, you're adding resistance to the system. Flow goes down, discharge pressure goes up, and you move left along the curve toward deadhead.

Be able to say that out loud, because it's an easy interview setup. They'll describe a valve position changing and ask what happens.

### Why you want to be near BEP

Everyone can repeat "stay near BEP" without knowing why, so knowing the actual reason is a cheap way to sound like you've been around this stuff. The short version is:

**The casing stops matching the flow.** The impeller spins inside a casing that isn't a circle, it's a spiral that widens as it wraps toward the discharge. That spiral is sized for BEP flow. At BEP, pressure around the outside of the impeller is even all the way around and the forces cancel out. Off BEP, pressure gets higher on one side than the other, and that imbalance is a net sideways push on the impeller. The impeller hangs off the end of the shaft past the bearings (think diving board), so a sideways push bends the shaft a little. That's what wears out bearings and mechanical seals, because a seal is two flat faces that only work if they stay lined up.

> [add visual here]

**The liquid stops hitting the vanes at the right angle.** Impeller vanes are shaped for liquid arriving one specific way, which again is BEP. Off design, the flow hits them at the wrong angle and separates off the vanes, and that's what causes internal recirculation.

> [add visual here]

Which way you've strayed changes how it fails:

**Too far left (low flow)** and you get internal recirculation plus heat buildup, because you're dumping shaft energy into a small amount of liquid that has nowhere to go. That's why pumps have a minimum flow spec and often a recirculation line back to the suction so you can throttle your discharge without endangering the pump.

**Too far right (toward runout)** and required NPSH (net positive suction head) goes up, so you're more likely to cavitate, and you can overload the motor.

Same underlying cause, two different ways to wreck the pump.

### NPSH without the textbook language

NPSH available is how much pressure margin the system is giving you at the suction, above the liquid's vapor pressure. NPSH required is how much the pump needs so the liquid doesn't vaporize inside it. Available has to be bigger than required.

When it isn't, you cavitate. Pressure at the impeller inlet drops below the liquid's vapor pressure, so the liquid boils and forms vapor bubbles. Those bubbles get carried through the impeller into a higher pressure region and collapse, and that collapse is violent enough to chip away at the metal. You lose flow, the pump vibrates, and it slowly eats its own impeller.

Flashing is the related failure that people mix up with it. Same starting point, the liquid vaporizes, but the vapor never gets back above vapor pressure so the bubbles don't collapse. They just carry through and out the discharge. You still lose flow, but you're not chewing up the impeller, so it's quieter and less destructive than cavitation.

Many pump problems turn out to be suction side problems. A plugged strainer, a low tank level, or a hotter-than-normal feed all eat into your NPSH available.

### Centrifugal vs. PD, and the part that actually matters

A centrifugal has a full curve. A PD pump basically gives you a constant flow rate no matter what the discharge pressure is, so its curve is close to vertical.

The practical consequence is the thing worth remembering:

The maximum pressure a centrifugal pump can ever put out is its suction pressure, plus the differential head at deadhead. Block the discharge and pressure climbs to that ceiling and stops there, so the system sees a known max.

A PD pump usually doesn't have one. Block the discharge on a gear, screw, reciprocating, or motor-driven metering pump and it will just keep making pressure until something breaks, which is why those need relief protection and centrifugals generally don't. An exception to this is air-operated diaphragm pumps, whose maximum pressures are dictated by the pressure of the supplied air.

So the better way to think about it isn't "centrifugal vs. PD," it's "what actually sets the ceiling here." On a centrifugal it's deadhead pressure. On an air-operated diaphragm pump it's whatever the air header is regulated to (so if that regulator is set high enough, you can still overpressure something downstream). On anything positively driven, there is no ceiling, and the answer is whatever fails first.

### If someone asks how you'd spec a pump

Stuff you'd need to know:

- Flow rate and head you need
- Fluid properties (viscosity, density, temperature, how corrosive it is)
- Materials of construction
- NPSH available in the system
- Centrifugal or PD, which mostly comes down to viscosity, how stable you need the flow, and pressure

High viscosity in particular tends to push you toward PD, because centrifugals lose efficiency badly on viscous fluids.

## Diagram

> [Two curves side by side. Left: centrifugal, head on y and flow on x, sloping down to the right, labeled with shutoff/deadhead at zero flow, BEP in the middle, runout at the far right, and a system curve overlaid with the operating point marked at the intersection. Right: PD, near vertical line showing flow basically independent of pressure, labeled "no pressure ceiling, needs relief protection."]

Seeing them next to each other makes the overpressure thing click without anyone having to explain it.

## Vocabulary

These get thrown around in conversation with zero explanation, so it's worth being able to use them naturally.

| Term | What it means |
|---|---|
| **Deadhead / shutoff head** | Zero flow, discharge blocked. The most pressure a centrifugal can make. |
| **Runout** | Far right of the curve. Max flow, min head. |
| **BEP** | Best efficiency point. Where the pump wants to operate. |
| **Minimum flow** | The lowest rate you can run at before heat and recirculation start doing damage. |
| **Recirculation line** | A line back to suction that keeps you above minimum flow. |
| **NPSHa / NPSHr** | Suction pressure margin you have vs. what the pump needs. Available has to beat required. |
| **Cavitation** | Liquid vaporizes at the low pressure suction and then the bubbles collapse violently once pressure comes back up inside the pump. Sounds like the pump is full of gravel. Eats the impeller. |
| **Flashing** | Liquid vaporizes and stays vapor through the pump, so you lose flow instead of chewing up metal. |
| **Dry running** | Pump running with no liquid in it. This kills seals very fast. |
| **Mechanical seal** | Seals the shaft where it goes into the casing. Very common failure point. |
| **Wear rings** | Replaceable clearance rings. As they wear you get more internal recirculation and the pump falls off its curve. |

## Troubleshooting

By far the most common symptom of a misbehaving pump is seeing that you’re not getting the flow that you should be.

What matters in an interview isn't rattling off causes, it's showing you have a robust method to find what the root cause is.

**1. Say what the problem actually is.** "The pump is broken" isn't a problem statement. "We're getting 400 gpm and we should be at 600" is.

**2. Figure out what normal looks like.** Pull the curve. Where should this pump be running given current system conditions? What was it doing last month? You can't call something abnormal without knowing what normal was.

**3. Come up with ideas, and look at the whole system, not just the pump.**

- Is it operating on its curve? If your discharge pressure and flow don't land on the curve, the pump itself has degraded.
- Is something blocked? Plugged suction strainer, a valve that's closed or partly closed, fouled line. Suction side restrictions also eat your NPSH.
- Is it a suction problem? Low tank level, hot feed, vapor binding. Check NPSH available.
- Is it cavitating? Go listen to it. Cavitation sounds like the pump is pumping gravel, and operators usually know before the instruments do.
- Did something in the system change? New lineup, different valve position, different feed.

**4. Go talk to people.** This is arguably the best approach for new engineers. This is the part nobody teaches you in school and it's most of the actual job.

- Have we had this issue on this pump before? Ask operations.
- When was it last overhauled? Ask maintenance.
- What's our long term strategy for this pump? Is it due, is it a known bad actor, is it spared? Ask maintenance/operations.
- What do the operators hear when they walk past it?

A huge amount of real troubleshooting is just going and getting knowledge that already exists somewhere in the organization. There was a great quote in my college reactions engineering textbook: “The next best thing to knowing something is knowing where to find it.”

**5. Decide what data would prove or kill each idea.** For everything on your list, what measurement would confirm or eliminate it? Suction and discharge pressure puts you on the curve. Differential pressure across the strainer tells you about plugging. Motor amps tell you about load. Then go get the data.

That last step is what separates someone thinking like an engineer from someone guessing, and in an interview, saying it out loud is often worth more than actually landing on the right answer.

## Cram sheet

Read this the night before.

- A pump pressurizes liquid. No pressure, no flow.
- Centrifugal has a full curve and head drops as flow rises. PD gives near constant flow regardless of pressure.
- Deadhead/shutoff is far left at zero flow, and it's the max pressure a centrifugal can make. Runout is far right at max flow. BEP is in the middle where you want to be.
- Close the discharge valve and flow goes down, pressure goes up, you move left on the curve. Open it and the opposite happens.
- Off BEP means uneven pressure around the impeller, radial thrust on the shaft, shaft deflection, and worn bearings and seals.
- Too far left is recirculation and heat. Too far right is higher NPSHr, cavitation, and motor overload.
- NPSHa has to beat NPSHr or else you cavitate. Most pump problems are suction side problems.
- Cavitation is bubbles forming and collapsing. Eats the impeller, sounds like gravel. Flashing is when those bubbles form but never collapse, sending vapor through the pump.
- Ask what sets the pressure ceiling. Centrifugal tops out at suction pressure + differential pressure at deadhead. Air-operated diaphragm pumps stall at about the air supply pressure. Anything positively driven (gear, screw, reciprocating, motor-driven metering) has no ceiling and needs relief protection.
- Not making rate? Check the curve, check for blockages, check suction, listen for cavitation, then go ask operations and maintenance what they know.
- Off the curve means a degraded pump, and wear rings and the impeller are usually the culprits.

## Questions people actually get asked

**"Where's the deadhead point on a pump curve?"**

Far left, zero flow. What they're really checking is whether you can read a curve at all, and whether you get that a centrifugal has a hard ceiling on the pressure it can make.

*More coming. If you got asked something good in a technical interview, send it in.*
