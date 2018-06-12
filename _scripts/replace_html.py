import os
import argparse

text = r'''
    <form
        class="call-in-answer-panel inline-form"
    >'''
replacement = r'''    <script id="check_answer">
      window.onload=function() {
        form = document.getElementsByClassName('call-in-answer-panel inline-form')[0]
        form.onsubmit=function() {
          right_answer = ''
          answer = document.getElementById('id_answer').value
          answer = normalize_puzzle_answer(answer)

          // Remove solved panel if it exists
          if (document.contains(document.getElementById('solved-panel'))) {
            document.getElementById("solved-panel").remove();
          }

          // Create new solved panel
          node = document.createElement('div')
          node.setAttribute('id', 'solved-panel')
          if (answer == right_answer) {
            node.setAttribute('class', 'solved-panel')
            node.innerHTML = "<h3>Solved!</h3>\n<p>The answer was <b>" + right_answer + "</b>.</p>"
          } else {
            node.setAttribute('class', 'solved-panel solved-panel--incorrect')
            node.innerHTML = "<h3>incorrect!</h3>"
          }

          // Inject it
          form.parentNode.insertBefore(node, form)

          // Return false to prevent GET request from executing
          return false;
        }
      }

      function normalize_puzzle_answer(answer) {
        return answer.toUpperCase().replace(/[^A-Z]/g, '')
      }
    </script>
    <form
            class="call-in-answer-panel inline-form"
        >'''



def main(info):
  for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
      if name.endswith('.html'):
        full_path = os.path.join(root, name)
        f = open(full_path, 'r')
        html = f.read()
        f.close()

        if text in html:
          print('Modifying {}'.format(full_path))
          if not info:
            html = html.replace(text, replacement)
            f = open(full_path, 'w')
            f.write(html)
            f.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i','--info',
    help='Show which files would be modified', action='store_true')
  args = parser.parse_args()
  main(args.info)
