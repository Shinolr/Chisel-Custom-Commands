#!/usr/bin/python

import fbchisellldbbase as fb

def lldbcommands():
  return [ PrintDataAsJSONString() ]

class PrintDataAsJSONString(fb.FBCommand):
    def name(self):
        return "pj"

    def description(self):
        return "Print JSON representation of Swift Data"

    def options(self):
        return [
            fb.FBCommandArgument(
                arg="plain",
                short="-p",
                long="--plain",
                boolean=True,
                default=False,
                help="Plain JSON",
            )
        ]

    def args(self):
        return [
            fb.FBCommandArgument(
                arg="object",
                type="NSObject *",
                help="The Swift Dictionary or Swift Array to print",
            )
        ]

    def run(self, arguments, options):
        # Convert to NSObject first to allow for objc runtime to process it
        nsData = fb.evaluateInputExpression(
            "{obj} as NSObject".format(obj=arguments[0])
        )

        jsonString = fb.evaluateExpressionValue(
            "(id)[[NSString alloc] initWithData:(NSData*){} encoding:4]".format(
               nsData
            )
        ).GetObjectDescription()

        print(jsonString)
